# ChatKit Frontend Implementation

## Overview
A complete Chat UI implementation integrated with the backend FastAPI server. The chat system allows users to communicate with an AI agent to manage tasks using natural language, with full conversation persistence to the database.

## Components & Features

### 1. Backend Database Models (`app/models.py`)
- **Conversation Model**: Stores chat conversations with timestamps and user association
  - Fields: id, owner_id (FK to User), title, created_at, updated_at
  - Relationship: One-to-many with Message and User models
  
- **Message Model**: Stores individual messages within conversations
  - Fields: id, role ('user' or 'assistant'), content, conversation_id (FK), created_at
  - Relationship: Many-to-one with Conversation

- **Response Models**: ConversationResponse and MessageResponse for API serialization

### 2. Backend Chat API (`app/routers/chat.py`)
Enhanced chat endpoints with database persistence:

**POST /chat/** - Send message and create/update conversation
- Creates new conversation if conversation_id not provided
- Saves both user and assistant messages to database
- Sets conversation title from first message
- Returns: message, conversation_id, conversation_history

**GET /chat/conversations** - Retrieve all user conversations
- Returns paginated list of conversations with message counts

**GET /chat/conversations/{id}** - Get specific conversation with all messages
- Includes all messages in conversation_history

**DELETE /chat/conversations/{id}** - Delete conversation and cascade delete messages

**GET /chat/health** - Health check endpoint

### 3. Frontend API Client (`frontend/src/lib/api.ts`)
Extended with chat functionality:
- `chatAPI.send()` - Send message with optional conversation_id
- `chatAPI.getConversations()` - Fetch all conversations
- `chatAPI.getConversation()` - Fetch single conversation
- `chatAPI.deleteConversation()` - Delete conversation

New TypeScript interfaces:
- `ChatMessage` - Message structure with role and content
- `ChatResponse` - API response with message and conversation_id
- `ConversationResponse` - Full conversation with metadata
- `MessageResponse` - Individual message data

### 4. Chat UI Component (`frontend/src/components/ChatUI.tsx`)
Beautiful, interactive chat interface:
- Real-time message display with user/assistant differentiation
- Auto-scrolling to latest messages
- Loading indicator with animated dots
- Error handling and display
- Clear chat functionality
- Mobile-responsive design
- Optimistic message addition for better UX

Features:
- Input validation and disabled state during loading
- Conversation history management
- Visual distinction between user (blue) and assistant (gray) messages
- Helpful placeholder with example queries

### 5. Chat Page (`frontend/src/app/chat/page.tsx`)
Full-featured chat interface:
- Two-column layout: Conversations sidebar + Chat area
- Conversations list showing:
  - Conversation title
  - Message count
  - Delete button (hover action)
- Navigation to tasks page
- Logout functionality
- "New Chat" button to start fresh conversation
- Loading states and error handling

## Data Flow

```
User Input
    ↓
ChatUI Component captures message
    ↓
Call chatAPI.send() with conversation_id (if exists)
    ↓
Backend creates/gets Conversation
    ↓
Backend calls AI agent (agent.py) to process request
    ↓
Backend saves user + assistant messages to DB
    ↓
Return response with conversation_id
    ↓
Frontend adds assistant message to display
    ↓
Update conversation_id if new conversation
    ↓
Display in ChatUI
    ↓
Save to conversations list when created
```

## Database Schema
```
User (1) ────── (Many) Conversation
         └─────────────────┤
                           ├─ id
                           ├─ owner_id (FK)
                           ├─ title
                           ├─ created_at
                           └─ updated_at
                           
Conversation (1) ────── (Many) Message
                        ├─ id
                        ├─ role
                        ├─ content
                        ├─ conversation_id (FK)
                        └─ created_at
```

## Authentication & Authorization
- All chat endpoints require JWT token (Bearer authentication)
- Conversations and messages are isolated per user
- Delete operations verify ownership before allowing deletion

## UI/UX Features
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Real-time Feedback**: Loading states, error messages
- **Message Formatting**: Proper spacing, word wrapping, truncation handling
- **Visual Hierarchy**: Color-coded messages, clear button states
- **Accessibility**: Semantic HTML, proper labels, keyboard support

## Integration Points
1. **Authentication Context**: Uses existing useAuth hook
2. **Task Management**: Chat page links to tasks page
3. **API Client**: Centralized axios instance with auth interceptors
4. **Conversation Persistence**: Automatic database saving
5. **Navigation**: Next.js router for page navigation

## Example Usage
1. User navigates to `/chat`
2. If not authenticated, redirects to `/login`
3. Chat page loads and displays existing conversations
4. User clicks "New Chat" or selects existing conversation
5. User types message and hits Send
6. Message appears immediately (optimistic)
7. API processes request and saves to database
8. Assistant response appears with conversation_id
9. Conversation appears in sidebar for future reference
10. User can delete conversations with delete button

## Error Handling
- Failed API requests show error message to user
- Optimistic messages are rolled back on error
- Conversation not found errors (404) handled gracefully
- Unauthorized requests redirect to login (401)
- Invalid message input is validated before sending

## Performance Optimizations
- Debounced conversation loading
- Lazy loading of conversation messages
- Optimistic UI updates
- Efficient re-rendering with proper React hooks usage
- Proper error recovery without full page reload

## Future Enhancements
- Export/download conversation history
- Share conversations with other users
- Search across conversations
- Conversation archiving instead of deletion
- Rich message formatting (markdown, code blocks)
- Message editing and deletion
- Typing indicators
- Read receipts
- Voice message support
