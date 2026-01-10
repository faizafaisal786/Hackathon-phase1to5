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

When users say:
- "add" or "create" - use add_task tool
- "show", "list", or "see" - use list_tasks tool
- "complete", "done", or "finish" - use complete_task tool
- "update" or "modify" - use update_task tool
- "delete" or "remove" - use delete_task tool

Be conversational and helpful. After performing an action, confirm what you did.
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


def parse_demo_command(message: str) -> tuple:
    """
    Parse user message in demo mode using simple pattern matching.
    Returns: (tool_name, arguments)
    """
    message_lower = message.lower().strip()

    # Add task
    if any(word in message_lower for word in ["add", "create", "new task"]):
        # Extract task title
        patterns = [
            r"(?:add|create|new)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)",
            r"(?:add|create)\s+(.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                title = match.group(1).strip()
                return ("add_task", {"title": title})
        return ("add_task", {"title": "New task"})

    # List tasks
    elif any(word in message_lower for word in ["show", "list", "display", "what", "see", "view"]):
        if "completed" in message_lower or "done" in message_lower:
            return ("list_tasks", {"status": "completed"})
        elif "pending" in message_lower:
            return ("list_tasks", {"status": "pending"})
        else:
            return ("list_tasks", {})

    # Complete task
    elif any(word in message_lower for word in ["complete", "done", "finish", "mark as complete"]):
        # Try to extract task ID or number
        match = re.search(r"(?:task|id)\s*[:#]?\s*([a-f0-9-]+)", message_lower)
        if match:
            return ("complete_task", {"id": match.group(1)})
        # Try to extract first/second/etc.
        match = re.search(r"(first|second|third|1st|2nd|3rd|\d+)", message_lower)
        if match:
            return ("complete_task", {"id": "by_position_" + match.group(1)})
        return (None, None)

    # Delete task
    elif any(word in message_lower for word in ["delete", "remove"]):
        match = re.search(r"(?:task|id)\s*[:#]?\s*([a-f0-9-]+)", message_lower)
        if match:
            return ("delete_task", {"id": match.group(1)})
        return (None, None)

    # Update task
    elif any(word in message_lower for word in ["update", "modify", "change", "edit"]):
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
        # Execute the tool
        result = execute_tool(tool_name, arguments)

        # Generate friendly response
        if tool_name == "add_task":
            response = f"I've added the task '{arguments.get('title', 'New task')}' to your list! {result}"
        elif tool_name == "list_tasks":
            status = arguments.get('status', 'all')
            response = f"Here are your {status} tasks:\n\n{result}"
        elif tool_name == "complete_task":
            response = f"Great job! {result}"
        elif tool_name == "delete_task":
            response = f"Task removed. {result}"
        elif tool_name == "update_task":
            response = f"Task updated. {result}"
        else:
            response = result
    else:
        response = (
            "I can help you manage your tasks! Try saying:\n"
            "- 'Add a task to buy groceries'\n"
            "- 'Show me my tasks'\n"
            "- 'Complete task ID: xyz'\n"
            "- 'Delete the first task'\n\n"
            f"(Running in FREE demo mode - no API key required)"
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
