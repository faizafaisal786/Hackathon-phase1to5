"""
Database models using SQLModel.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class UserBase(SQLModel):
    """Base user model with shared fields."""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = None


class User(UserBase, table=True):
    """User database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships with tasks and conversations
    tasks: list["Task"] = Relationship(back_populates="owner")
    conversations: list["Conversation"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserResponse(UserBase):
    """User response schema (without password)."""
    id: int
    is_active: bool
    created_at: datetime


class Token(SQLModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"


class LoginRequest(SQLModel):
    """Login request schema."""
    username: str
    password: str


class TaskBase(SQLModel):
    """Base task model with shared fields."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with user
    owner: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(SQLModel):
    """Task update schema (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class Token(SQLModel):
    """JWT token response."""
    access_token: str
    token_type: str


class TokenData(SQLModel):
    """Token payload data."""
    user_id: Optional[int] = None


class LoginRequest(SQLModel):
    """Login request schema."""
    username: str
    password: str


class MessageBase(SQLModel):
    """Base message model with shared fields."""
    role: str  # 'user' or 'assistant'
    content: str


class Message(MessageBase, table=True):
    """Message database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageResponse(MessageBase):
    """Message response schema."""
    id: int
    conversation_id: int
    created_at: datetime


class ConversationBase(SQLModel):
    """Base conversation model with shared fields."""
    title: Optional[str] = None


class Conversation(ConversationBase, table=True):
    """Conversation database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: Optional[User] = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# Update forward references
SQLModel.update_forward_refs()


class ConversationCreate(ConversationBase):
    """Conversation creation schema."""
    pass


class ConversationResponse(ConversationBase):
    """Conversation response schema."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse] = []