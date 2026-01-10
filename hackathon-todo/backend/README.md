# Backend Services

This directory contains the backend services for the todo application, including:
- MCP Server (Model Context Protocol)
- OpenAI Agent Integration
- Task Management Functions

## Files

- **mcp_server.py**: MCP server that exposes task management tools
- **agent.py**: OpenAI Agents SDK integration for natural language task management
- **tasks.py**: Core task management functions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in the root `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

## MCP Server

The MCP server exposes task management tools that can be used by any MCP-compatible client.

### Available Tools

- `add_task`: Add a new task
- `list_tasks`: List all tasks (with optional status filter)
- `update_task`: Update an existing task
- `delete_task`: Delete a task
- `complete_task`: Mark a task as completed

### Running the MCP Server

```bash
cd backend
python mcp_server.py
```

The server runs over stdio and can be connected to from any MCP client.

### MCP Client Configuration

To use this server with Claude Desktop or other MCP clients, add this configuration to your MCP settings:

```json
{
  "mcpServers": {
    "todo": {
      "command": "python",
      "args": ["path/to/backend/mcp_server.py"]
    }
  }
}
```

## OpenAI Agent

The OpenAI agent provides a natural language interface for task management using OpenAI's function calling capabilities.

### Features

- Natural language task management
- Automatic tool selection based on user intent
- Conversational interface
- Context-aware responses

### Usage

```python
from agent import chat, simple_chat

# Simple usage (no conversation history)
response = simple_chat("Add a task to buy groceries")
print(response)

# With conversation history
result = chat("Show me all my tasks", conversation_history=[])
print(result["message"])
print(result["conversation_history"])
```

### Testing the Agent

```bash
cd backend
python agent.py
```

This will run some test conversations with the agent.

## REST API Integration

The agent is integrated into the main FastAPI application via the `/chat` endpoint.

### Chat Endpoint

**POST /chat/**

Request:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_history": []
}
```

Response:
```json
{
  "message": "I've added the task 'buy groceries' to your todo list.",
  "conversation_history": [...]
}
```

### Example Usage

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

## Task Storage

Tasks are stored in a `tasks.json` file in the backend directory. This is a simple file-based storage system suitable for development and testing.

For production use, consider integrating with the main application's PostgreSQL database.

## Development

### Adding New Tools

1. Add the function to `tasks.py`
2. Add the tool definition to `mcp_server.py` (for MCP)
3. Add the tool definition to `agent.py` (for OpenAI agent)
4. Update the tool execution logic in both files

### Testing

```bash
# Test the agent
python agent.py

# Test the MCP server (requires MCP client)
python mcp_server.py
```

## Integration with Main App

The chat endpoint in `app/routers/chat.py` integrates the agent with the main FastAPI application. This allows:

- RESTful API access to the agent
- Potential for adding authentication
- Integration with the existing task database
- Frontend chat interface

## Future Enhancements

- [ ] Integrate with main PostgreSQL database instead of tasks.json
- [ ] Add authentication to chat endpoint
- [ ] Support for streaming responses
- [ ] Add memory/context persistence
- [ ] Support for task attachments and tags
- [ ] Natural language search and filtering
