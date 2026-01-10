"""
Chat endpoint for the AI agent.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from sqlmodel import Session, select

# Add backend directory to path to import agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))
from agent import chat
from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, Conversation, Message, ConversationResponse, MessageResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


class ChatMessage(BaseModel):
    """Message model for chat requests."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None
    conversation_history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str
    conversation_id: int
    conversation_history: List[dict]


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Chat with the AI agent to manage tasks.

    This endpoint uses OpenAI's function calling to automatically
    execute task management operations based on natural language.

    Example requests:
    - "Add a task to buy groceries"
    - "Show me all my tasks"
    - "Complete the task with ID xyz"
    - "Delete the grocery task"
    """
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.owner_id != current_user.id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(owner_id=current_user.id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Process chat request with the AI agent
        result = chat(request.message, request.conversation_history)
        
        # Save user message
        user_message = Message(
            role="user",
            content=request.message,
            conversation_id=conversation.id
        )
        session.add(user_message)
        
        # Save assistant message
        assistant_message = Message(
            role="assistant",
            content=result["message"],
            conversation_id=conversation.id
        )
        session.add(assistant_message)
        
        # Update conversation title if it's the first message
        if not conversation.title and len(result["conversation_history"]) == 2:
            conversation.title = request.message[:50]  # Use first message as title
        
        session.commit()
        session.refresh(conversation)
        
        return ChatResponse(
            message=result["message"],
            conversation_id=conversation.id,
            conversation_history=result["conversation_history"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all conversations for the current user."""
    statement = select(Conversation).where(Conversation.owner_id == current_user.id)
    conversations = session.exec(statement).all()
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific conversation with all messages."""
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a conversation."""
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    session.delete(conversation)
    session.commit()
    return {"message": "Conversation deleted"}


@router.get("/health")
async def chat_health():
    """Health check for chat endpoint."""
    return {"status": "healthy", "service": "chat"}

