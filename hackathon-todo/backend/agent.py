"""
OpenAI Agents SDK integration for the todo app.
Supports both OpenAI API and FREE demo mode.
"""
import os
import re
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Add backend directory to path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from tasks import add_task, list_tasks, update_task, delete_task, complete_task

# Load environment variables
load_dotenv()

# Initialize OpenAI client (lazy initialization)
_client = None
_demo_mode = None

def get_demo_mode():
    """Check if running in demo mode (no API key required)."""
    global _demo_mode
    if _demo_mode is None:
        api_key = os.getenv("OPENAI_API_KEY")
        _demo_mode = not api_key or api_key == "demo" or api_key.startswith("demo-")
    return _demo_mode

def get_client():
    """Get or create OpenAI client."""
    global _client
    if _client is None:
        if get_demo_mode():
            return None  # Demo mode, no client needed
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file or use 'demo' for demo mode."
            )
        _client = OpenAI(api_key=api_key)
    return _client

# Define the tools for the agent
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date for the task (optional)"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks, optionally filtered by status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status: 'pending' or 'completed'",
                        "enum": ["", "pending", "completed"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date for the task"
                    }
                },
                "required": ["id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "ID of the task to mark as completed"
                    }
                },
                "required": ["id"]
            }
        }
    }
]

# Tool execution mapping
TOOL_FUNCTIONS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "update_task": update_task,
    "delete_task": delete_task,
    "complete_task": complete_task
}

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list.
You understand both English and Hindi/Hinglish commands.

When users say:
- "add", "create", "add kar", "add karo", "add kar do", "kaam add" - use add_task tool
- "show", "list", "see", "dikha", "dikhao" - use list_tasks tool
- "complete", "done", "finish", "poora", "khatam" - use complete_task tool
- "update", "modify", "change" - use update_task tool
- "delete", "remove", "hata", "hatao" - use delete_task tool

Date handling:
- "kal ka" / "tomorrow" means task due tomorrow
- "parso" / "day after tomorrow" means task due in 2 days
- "aaj ka" / "today" means task due today

When user says "Kal ka kaam add kar do" or similar, automatically extract:
- Title: "kaam" or the actual task description
- Due date: tomorrow's date

Be conversational and helpful. After performing an action, confirm what you did in a friendly way.
"""


def execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute a tool function with the given arguments."""
    try:
        func = TOOL_FUNCTIONS.get(tool_name)
        if not func:
            return f"Unknown tool: {tool_name}"

        # Call the function with unpacked arguments
        if tool_name == "add_task":
            result = func(
                arguments.get("title", ""),
                arguments.get("description", ""),
                arguments.get("due_date", "")
            )
        elif tool_name == "list_tasks":
            result = func(arguments.get("status", ""))
        elif tool_name == "update_task":
            result = func(
                arguments["id"],
                arguments.get("title", ""),
                arguments.get("description", ""),
                arguments.get("due_date", "")
            )
        elif tool_name in ["delete_task", "complete_task"]:
            result = func(arguments["id"])
        else:
            result = f"Unknown tool: {tool_name}"

        return result
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"


def parse_date_from_message(message: str) -> str:
    """
    Parse date from message (supports Hindi/English).
    Returns: ISO format date string or empty string
    """
    message_lower = message.lower()
    today = datetime.now()
    
    # Hindi/Hinglish date patterns
    if any(word in message_lower for word in ["kal", "tomorrow", "kal ka", "tomorrow's"]):
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")
    elif any(word in message_lower for word in ["parso", "day after tomorrow"]):
        day_after = today + timedelta(days=2)
        return day_after.strftime("%Y-%m-%d")
    elif any(word in message_lower for word in ["aaj", "today", "aaj ka"]):
        return today.strftime("%Y-%m-%d")
    elif any(word in message_lower for word in ["agle hafte", "next week"]):
        next_week = today + timedelta(days=7)
        return next_week.strftime("%Y-%m-%d")
    elif any(word in message_lower for word in ["agle mahine", "next month"]):
        next_month = today + timedelta(days=30)
        return next_month.strftime("%Y-%m-%d")
    
    # Try to parse specific dates (simple format: DD-MM-YYYY or YYYY-MM-DD)
    date_patterns = [
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",  # DD-MM-YYYY or DD/MM/YYYY
        r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})",    # YYYY-MM-DD or YYYY/MM/DD
    ]
    for pattern in date_patterns:
        match = re.search(pattern, message)
        if match:
            try:
                date_str = match.group(1)
                # Try to parse common formats
                for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%y", "%d/%m/%y"]:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        return parsed_date.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
            except:
                pass
    
    return ""


def parse_demo_command(message: str) -> tuple:
    """
    Parse user message in demo mode using simple pattern matching.
    Supports Hindi/Hinglish commands.
    Returns: (tool_name, arguments)
    """
    message_lower = message.lower().strip()
    original_message = message.strip()

    # Friendly greetings and help
    greetings = ["hello", "hi", "hey", "help", "what can you do", "kya kar sakte", "madad"]
    if any(word in message_lower for word in greetings) and not any(word in message_lower for word in ["add", "show", "task", "complete", "delete"]):
        return ("help", {})

    # Planning/suggestion requests
    planning_words = ["what should i do", "plan my day", "suggest", "help me plan", "kya karun", "important"]
    if any(word in message_lower for word in planning_words):
        return ("suggest", {})

    # Add task - Hindi/Hinglish support
    if any(word in message_lower for word in ["add", "create", "new task", "add kar", "add karo", "add kar do",
                                               "kaam add", "task add", "add kaam", "remind me"]):
        # Extract description if present
        description = ""
        title_part = original_message

        # Check for "Description:" pattern
        desc_match = re.search(r"[.]\s*description[:\s]+(.+)", original_message, re.IGNORECASE)
        if desc_match:
            description = desc_match.group(1).strip()
            title_part = original_message[:desc_match.start()]

        # Extract task title
        title_message = title_part.lower()
        for date_word in ["kal ka", "kal", "tomorrow", "tomorrow's", "parso", "aaj ka", "today", "remind me to", "remind me"]:
            title_message = re.sub(rf"\b{date_word}\b", "", title_message, flags=re.IGNORECASE)

        patterns = [
            r"(?:add|create|new)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)",
            r"(?:add|create|kar|karo|kar\s+do)\s+(.+)",
            r"(?:kaam|task)\s+add\s+(.+)",
            r"add\s+(?:kar|karo|kar\s+do)\s+(.+)",
        ]

        title = "New task"
        for pattern in patterns:
            match = re.search(pattern, title_message)
            if match:
                title = match.group(1).strip()
                # Clean up common Hindi/English filler words
                title = re.sub(r"\b(ka|ko|kaa|kii|kar|karo|kar\s+do|do|kaam|task|add)\b", "", title, flags=re.IGNORECASE).strip()
                title = re.sub(r"\s+", " ", title)
                if title:
                    break

        # Capitalize first letter
        if title and title != "New task":
            title = title[0].upper() + title[1:] if len(title) > 1 else title.upper()

        # Extract due date
        due_date = parse_date_from_message(message)

        return ("add_task", {"title": title, "description": description, "due_date": due_date})

    # List tasks - Hindi/Urdu support
    elif any(word in message_lower for word in ["show", "list", "display", "what", "see", "view",
                                                  "dikhao", "dikha", "batao", "bata", "tasks", "kaam"]):
        if "completed" in message_lower or "done" in message_lower or "mukammal" in message_lower or "complete" in message_lower:
            return ("list_tasks", {"status": "completed"})
        elif "pending" in message_lower or "baqi" in message_lower:
            return ("list_tasks", {"status": "pending"})
        else:
            return ("list_tasks", {})

    # Complete task - Hindi/Urdu support
    elif any(word in message_lower for word in ["complete", "done", "finish", "mark as complete",
                                                  "mukammal", "khatam", "ho gaya", "kar diya", "poora"]):
        # Try to extract task ID or number
        match = re.search(r"(?:task|id|kaam)\s*[:#]?\s*([a-f0-9-]+)", message_lower)
        if match:
            return ("complete_task", {"id": match.group(1)})
        # Try to extract first/second/etc.
        match = re.search(r"(first|second|third|1st|2nd|3rd|pehla|doosra|teesra|\d+)", message_lower)
        if match:
            return ("complete_task", {"id": "by_position_" + match.group(1)})
        return (None, None)

    # Delete task - Hindi/Urdu support
    elif any(word in message_lower for word in ["delete", "remove", "hata", "hatao", "mitao", "mita"]):
        match = re.search(r"(?:task|id|kaam)\s*[:#]?\s*([a-f0-9-]+)", message_lower)
        if match:
            return ("delete_task", {"id": match.group(1)})
        return (None, None)

    # Update task - Hindi/Urdu support
    elif any(word in message_lower for word in ["update", "modify", "change", "edit", "badal", "badlo"]):
        match = re.search(r"(?:task|id)\s*[:#]?\s*([a-f0-9-]+)", message_lower)
        if match:
            return ("update_task", {"id": match.group(1)})
        return (None, None)

    return (None, None)


def chat_demo_mode(message: str, conversation_history: list = None) -> dict:
    """
    Process chat in FREE demo mode without OpenAI API.
    Uses simple pattern matching to understand commands.
    """
    if conversation_history is None:
        conversation_history = []

    # Add user message
    conversation_history.append({
        "role": "user",
        "content": message
    })

    # Parse command
    tool_name, arguments = parse_demo_command(message)

    if tool_name:
        # Handle special commands
        if tool_name == "help":
            response = (
                "🤖 **AI Task Assistant**\n\n"
                "Hello! I can help you manage your tasks. Here's what I can do:\n\n"
                "**➕ Add Tasks:**\n"
                "• 'Add task Buy groceries'\n"
                "• 'Add task Learn Docker. Description: Practice commands'\n"
                "• 'Kal ka kaam add karo meeting'\n\n"
                "**📋 View Tasks:**\n"
                "• 'Show my tasks'\n"
                "• 'What tasks are pending?'\n"
                "• 'Tasks dikhao'\n\n"
                "**✅ Complete Tasks:**\n"
                "• 'Complete task [ID]'\n"
                "• 'Mark Buy groceries as done'\n\n"
                "**🗑️ Delete Tasks:**\n"
                "• 'Delete task [ID]'\n"
                "• 'Remove task homework'\n\n"
                "💡 I understand English, Hindi & Urdu!"
            )
        elif tool_name == "suggest":
            # Get tasks and suggest
            tasks_result = execute_tool("list_tasks", {"status": "pending"})
            response = (
                "💡 **Here's my suggestion for today:**\n\n"
                f"{tasks_result}\n\n"
                "🎯 **Tips:**\n"
                "• Start with high priority tasks first\n"
                "• Break big tasks into smaller ones\n"
                "• Take short breaks between tasks\n\n"
                "Need to add more tasks? Just say 'Add task [your task]'"
            )
        else:
            # Execute the tool
            result = execute_tool(tool_name, arguments)

            # Generate friendly response
            if tool_name == "add_task":
                due_info = ""
                desc_info = ""
                if arguments.get('due_date'):
                    due_info = f"\n📅 Due: {arguments.get('due_date')}"
                if arguments.get('description'):
                    desc_info = f"\n📝 {arguments.get('description')}"
                response = f"✅ Task added successfully!\n\n**{arguments.get('title', 'New task')}**{desc_info}{due_info}\n\nSay 'show tasks' to see all your tasks."
            elif tool_name == "list_tasks":
                status = arguments.get('status', 'all')
                response = f"📋 Your {status} tasks:\n\n{result}"
            elif tool_name == "complete_task":
                response = f"🎉 Great job! Task marked as complete!\n\n{result}"
            elif tool_name == "delete_task":
                response = f"🗑️ Task deleted successfully!\n\n{result}"
            elif tool_name == "update_task":
                response = f"✏️ Task updated successfully!\n\n{result}"
            else:
                response = result
    else:
        response = (
            "🤖 **AI Task Assistant**\n\n"
            "I can help you manage your tasks! Try these commands:\n\n"
            "**English:**\n"
            "• Add task buy groceries\n"
            "• Show my tasks\n"
            "• Complete task [ID]\n\n"
            "**Hindi/Urdu:**\n"
            "• Kal ka kaam add karo meeting\n"
            "• Tasks dikhao\n"
            "• Pending kaam batao\n\n"
            "💡 I understand natural language in English, Hindi & Urdu!"
        )

    # Add assistant response
    conversation_history.append({
        "role": "assistant",
        "content": response
    })

    return {
        "message": response,
        "conversation_history": conversation_history
    }


def chat(message: str, conversation_history: list = None) -> dict:
    """
    Process a chat message using OpenAI's function calling or demo mode.

    Args:
        message: User's message
        conversation_history: Previous messages in the conversation

    Returns:
        dict: Response containing the assistant's message and updated conversation history
    """
    # Use demo mode if no API key
    if get_demo_mode():
        return chat_demo_mode(message, conversation_history)

    if conversation_history is None:
        conversation_history = []

    # Add system prompt if this is the first message
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

    # Add user message
    conversation_history.append({
        "role": "user",
        "content": message
    })

    # Get OpenAI client
    client = get_client()

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        tools=TOOLS,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Add assistant's response to conversation history
    conversation_history.append(response_message)

    # If the model wants to call a tool
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = eval(tool_call.function.arguments)

            # Execute the tool
            function_response = execute_tool(function_name, function_args)

            # Add tool response to conversation
            conversation_history.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })

        # Get final response from the model
        second_response = get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )

        final_message = second_response.choices[0].message
        conversation_history.append(final_message)

        return {
            "message": final_message.content,
            "conversation_history": conversation_history
        }
    else:
        return {
            "message": response_message.content,
            "conversation_history": conversation_history
        }


def simple_chat(message: str) -> str:
    """
    Simple chat interface that returns just the response message.

    Args:
        message: User's message

    Returns:
        str: Assistant's response
    """
    result = chat(message)
    return result["message"]


if __name__ == "__main__":
    # Test the agent
    print("Todo Agent Chat Test")
    print("=" * 50)

    test_messages = [
        "Add a task to buy groceries",
        "Show me all my tasks",
        "What tasks do I have?"
    ]

    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = simple_chat(msg)
        print(f"Agent: {response}")
