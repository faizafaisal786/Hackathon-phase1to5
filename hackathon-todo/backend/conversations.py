from datetime import datetime
from typing import List, Tuple

# Use in-memory storage for Vercel serverless deployment
# Note: This means conversations will be lost on function cold starts
# For production, use a proper database (PostgreSQL, MongoDB, etc.)
conversations = {}

def init_db():
    """Initialize database (no-op for in-memory storage)"""
    pass

def save_message(conversation_id: str, role: str, content: str):
    """Save a message to in-memory storage"""
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    conversations[conversation_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

def get_conversation(conversation_id: str) -> List[Tuple[str, str]]:
    """Get conversation messages from in-memory storage"""
    if conversation_id not in conversations:
        return []

    # Return as list of tuples (role, content) to match original interface
    return [(msg["role"], msg["content"]) for msg in conversations[conversation_id]]