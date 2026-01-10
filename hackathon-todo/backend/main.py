from fastapi import FastAPI
from pydantic import BaseModel
from agents import Agent, function_tool
from tasks import add_task, list_tasks, update_task, delete_task, complete_task
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_tool = function_tool(add_task)
list_tool = function_tool(list_tasks)
update_tool = function_tool(update_task)
delete_tool = function_tool(delete_task)
complete_tool = function_tool(complete_task)

agent = Agent(
    name="TodoAgent",
    instructions="You are a helpful assistant for managing todo tasks. Use the available tools to add, list, update, delete, and complete tasks.",
    tools=[add_tool, list_tool, update_tool, delete_tool, complete_tool],
    model="gpt-4o"
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    response = await agent.run(request.message)
    # Save conversation (implement in conversations.py)
    from conversations import save_message
    save_message(request.conversation_id, "user", request.message)
    save_message(request.conversation_id, "assistant", response)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)