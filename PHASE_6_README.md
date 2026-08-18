# PHASE 6: AI Student & Career Chatbot + Knowledge Base

## Overview

PHASE 6 adds a comprehensive AI-powered chatbot system that provides personalized guidance on:
- Career guidance and internship preparation
- Learning path recommendations
- Skill assessment and improvement
- Concept explanations and practice suggestions
- Project ideas based on skill level

The chatbot integrates with existing student data (profile, skills, projects, career goals, assessment results) to provide context-aware responses without requiring external API keys.

## Features Implemented

### 1. AI Student & Career Chatbot UI
- **Location**: `chat.html`
- Modern, mobile-responsive chat interface
- Chat history sidebar for managing conversations
- Real-time message updates with loading indicators
- Message formatting with markdown-like support
- Student context display

### 2. Knowledge Base System
- **File**: `backend/knowledge_base.py`
- 9 pre-loaded educational documents covering:
  - Web Development (REST API, etc.)
  - Database Design and SQL
  - Python Backend Development
  - Cybersecurity Fundamentals
  - Linux Command Line
  - Machine Learning Basics
  - Career Guidance
  - Interview Preparation
  - Cloud Computing
- Searchable by keywords, categories, and difficulty level
- RAG-ready architecture for future embeddings integration

### 3. AI Service Abstraction
- **File**: `backend/ai_service.py`
- Pluggable AI provider system
- LocalAIProvider implementation (no external APIs required)
- Intent detection (career guidance, learning guidance, skill assessment, etc.)
- Context-aware response generation
- Ready for integration with OpenAI, Anthropic, or other LLMs

### 4. Chatbot Logic & Context Builder
- **File**: `backend/chatbot_logic.py`
- StudentContextBuilder: Aggregates student data for AI
- Missing skills calculation based on career goal
- Student context summary for personalization
- Skill level assessment

### 5. Chat API Endpoints
- **In**: `backend/main.py`
- REST endpoints for chat operations:
  - `POST /api/chat/new` - Create new chat
  - `GET /api/chat/list` - List all conversations
  - `GET /api/chat/{chat_id}` - Get specific chat with messages
  - `POST /api/chat/{chat_id}/message` - Send message and get AI response
  - `DELETE /api/chat/{chat_id}` - Delete chat
  - `DELETE /api/chat/{chat_id}/clear` - Clear messages
  - `GET /api/chat/context` - Get student context

### 6. Database Models
- **In**: `backend/models.py`
- `Chat` model: Stores conversation metadata
- `ChatMessage` model: Stores individual messages
- Proper user relationships and cascading deletes

### 7. Dashboard Integration
- Added PHASE 6 section to `dashboard.html`
- Chatbot card with description
- "Open AI Assistant" button linking to chat.html

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database
The database is automatically created when the backend starts for the first time.

### 3. Start the Backend
```bash
cd backend
python start_backend.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Start the Frontend
```bash
npm install
npm run dev
```

### 5. Access the Chatbot
- Log in to the platform
- Go to Dashboard
- Click "Open AI Assistant" in the PHASE 6 section
- Or navigate directly to `http://localhost:5173/chat.html`

## How to Use

### Starting a Conversation
1. Click "New Chat" to start a fresh conversation
2. Type your question in the message input
3. Press Enter (or Shift+Enter for new lines)
4. View the AI response

### Questions You Can Ask

**Career Guidance:**
- "What career is suitable for me?"
- "What skills do I need for cybersecurity?"
- "Am I ready for a backend internship?"
- "Which role matches my current skills?"

**Learning Guidance:**
- "Explain REST API in simple words"
- "What should I learn next?"
- "How can I prepare for interviews?"
- "Suggest project ideas for my level"

**Skill Assessment:**
- "What is my current skill level in Python?"
- "How can I improve my programming skills?"
- "What skills am I missing for my career goal?"

**General Questions:**
- "Tell me about databases"
- "What is machine learning?"
- "How does cloud computing work?"

## Architecture

### How It Works

```
User Question
    ↓
Chat API (/api/chat/{chat_id}/message)
    ↓
ChatbotLogic.process_message()
    ↓
StudentContextBuilder (builds student context from DB)
    ↓
AIService.chat()
    ↓
LocalAIProvider (generates response)
    ├─ Intent Detection
    ├─ Knowledge Base Search
    └─ Context-Aware Response
    ↓
Response saved to ChatMessage
    ↓
User receives response in chat UI
```

### Data Flow

1. **Student Context** is built from:
   - User profile (university, branch, year, etc.)
   - Skills and proficiency levels
   - Projects and experience
   - Career goals and preferences
   - Assessment results and skill levels
   - Missing skills (calculated)

2. **AI Response** is generated based on:
   - User intent detection
   - Student context
   - Knowledge base documents
   - Domain-specific rules

3. **Chat History** is stored:
   - One chat per conversation
   - Messages linked to user
   - Timestamps for ordering
   - Role (user/assistant) for formatting

## Extending the System

### Adding Custom AI Provider

```python
from ai_service import AIProvider

class CustomAIProvider(AIProvider):
    async def generate_response(self, user_message, conversation_context):
        # Your implementation
        return {"response": "...", "context_used": {...}}

# In main.py
from ai_service import ai_service, CustomAIProvider
ai_service.set_provider(CustomAIProvider())
```

### Adding More Knowledge Base Documents

```python
from knowledge_base import KnowledgeDocument, kb

doc = KnowledgeDocument(
    title="Your Topic",
    category="Your Category",
    content="Your educational content...",
    keywords=["keyword1", "keyword2"],
    difficulty="Beginner"
)
kb.add_document(doc)
```

### Integrating with OpenAI

```python
import openai
from ai_service import AIProvider

class OpenAIProvider(AIProvider):
    async def generate_response(self, user_message, conversation_context):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[...]
        )
        return {"response": response.choices[0].message.content}
```

## Future Enhancements

1. **Vector Search**
   - Integrate Pinecone or Weaviate
   - Use embeddings for better document retrieval
   - Semantic similarity search

2. **Real LLM Integration**
   - Connect to OpenAI GPT-4
   - Anthropic Claude
   - Hugging Face models

3. **Advanced Features**
   - Multi-turn conversation understanding
   - Follow-up question handling
   - Conversation analytics
   - Chat export/sharing

4. **Personalization**
   - Learning style adaptation
   - Difficulty adjustment
   - Preferred language support
   - Custom knowledge base per organization

## Security Considerations

- ✅ User authentication required for all chat endpoints
- ✅ Chat data is user-specific (no cross-user data leakage)
- ✅ Input validation on all message submissions
- ✅ No sensitive data in knowledge base
- ✅ CORS properly configured

## Troubleshooting

### Chat not loading
- Ensure backend is running on http://localhost:8000
- Check browser console for errors
- Verify JWT token is valid

### AI response takes too long
- LocalAIProvider should respond instantly
- Check for database query issues
- Review server logs

### Messages not saved
- Verify database connection
- Check user authentication
- Review API response status

## API Documentation

### Create New Chat
```
POST /api/chat/new
Headers: Authorization: Bearer {token}
Response: { "id": 1, "title": "New Conversation", "created_at": "...", "updated_at": "..." }
```

### Send Message
```
POST /api/chat/{chat_id}/message
Headers: Authorization: Bearer {token}
Body: { "content": "Your question here" }
Response: {
  "user_message": { "id": 1, "role": "user", "content": "...", "created_at": "..." },
  "ai_response": { "id": 2, "role": "assistant", "content": "...", "created_at": "..." }
}
```

### Get Chat History
```
GET /api/chat/{chat_id}
Headers: Authorization: Bearer {token}
Response: { "id": 1, "title": "...", "messages": [...], "created_at": "...", "updated_at": "..." }
```

### List All Chats
```
GET /api/chat/list
Headers: Authorization: Bearer {token}
Response: { "chats": [...] }
```

## Testing

### Manual Testing Checklist
- [ ] Create new chat
- [ ] Send career guidance question
- [ ] Send learning guidance question
- [ ] Check message history loads
- [ ] Delete a chat
- [ ] Clear chat messages
- [ ] Test on mobile device
- [ ] Verify student context is correct
- [ ] Test with different user accounts
- [ ] Verify no data leakage between users

### Example Test Flow
1. Login as student
2. Go to Dashboard → Open AI Assistant
3. Ask: "What skills should I learn for backend development?"
4. Verify response considers student's current skills
5. Ask: "How do I prepare for internships?"
6. Verify response uses knowledge base
7. Create new chat, repeat different questions
8. Verify separate conversations
9. Delete a chat
10. Verify it's removed from list

## Performance Notes

- LocalAIProvider has instant response times
- Database queries are optimized for student context
- Knowledge base search is in-memory and fast
- Chat history loads efficiently

## File Locations

```
student-support-platform/
├── chat.html                    # Chat UI
├── dashboard.html               # Updated with PHASE 6 card
├── backend/
│   ├── main.py                 # Updated with chat endpoints
│   ├── models.py               # Updated with Chat/ChatMessage
│   ├── schemas.py              # Updated with chat schemas
│   ├── ai_service.py           # NEW: AI provider abstraction
│   ├── knowledge_base.py        # NEW: Knowledge base system
│   ├── chatbot_logic.py         # NEW: Chatbot coordination
│   └── requirements.txt         # Already has dependencies
```

## Notes

- PHASE 6 does NOT require external API keys
- All features work with local resources
- Clean architecture allows easy integration with real LLMs
- Knowledge base is RAG-ready for embeddings
- No existing features are broken
- All user data is properly isolated

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs
3. Check browser console for frontend errors
4. Verify database connection
5. Ensure all dependencies are installed

---

**PHASE 6 Status**: ✅ Complete and Ready for Testing
