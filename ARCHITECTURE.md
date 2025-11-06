# 🏗️ AutoQuery Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                    (Browser - localhost:5173)                       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + TypeScript)                  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   App.tsx    │  │ ChatMessage  │  │  ChatInput   │            │
│  │ (Main Logic) │  │  Component   │  │  Component   │            │
│  └──────┬───────┘  └──────────────┘  └──────────────┘            │
│         │                                                          │
│         │                                                          │
│  ┌──────▼───────────────────────────────────────────┐            │
│  │         API Service (api.ts)                      │            │
│  │  - chatAPI.sendMessage()                          │            │
│  │  - documentsAPI.upload()                          │            │
│  └───────────────────────────────────────────────────┘            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ Axios HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI - Python)                       │
│                      (localhost:8000)                               │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                     API Routes                              │  │
│  │  ┌────────────────┐         ┌────────────────┐             │  │
│  │  │  /api/chat     │         │ /api/documents │             │  │
│  │  │  - /message    │         │  - /upload     │             │  │
│  │  │  - /stream     │         │  - /list       │             │  │
│  │  │  - /session    │         │  - /delete     │             │  │
│  │  └────────┬───────┘         └───────┬────────┘             │  │
│  └───────────┼─────────────────────────┼──────────────────────┘  │
│              │                         │                          │
│              ▼                         ▼                          │
│  ┌───────────────────────┐   ┌──────────────────────┐          │
│  │   LLM Service         │   │  Document Service    │          │
│  │  (llm_service.py)     │   │ (document_service.py)│          │
│  │                       │   │                       │          │
│  │  - chat()             │   │ - process_document() │          │
│  │  - chat_stream()      │   │ - search_documents() │          │
│  └───────────┬───────────┘   └───────────┬──────────┘          │
└──────────────┼───────────────────────────┼─────────────────────────┘
               │                           │
               │                           │
               ▼                           ▼
┌──────────────────────┐      ┌────────────────────────┐
│   OpenAI API         │      │  Document Processing   │
│   (GPT-4)            │      │                        │
│                      │      │  ┌──────────────────┐  │
│  - Chat completions  │      │  │  Text Extraction │  │
│  - Embeddings        │      │  │  - PyPDF2        │  │
│  - Streaming         │      │  │  - python-docx   │  │
└──────────────────────┘      │  │  - Plain text    │  │
                              │  └────────┬─────────┘  │
                              │           │             │
                              │  ┌────────▼─────────┐  │
                              │  │  Text Chunking   │  │
                              │  │  (LangChain)     │  │
                              │  └────────┬─────────┘  │
                              │           │             │
                              │  ┌────────▼─────────┐  │
                              │  │  Vector Store    │  │
                              │  │  (FAISS)         │  │
                              │  └──────────────────┘  │
                              └────────────────────────┘
```

---

## Data Flow - User Asks a Question

```
1. USER TYPES QUESTION
   │
   ├─→ "What is the refund policy?"
   │
   ▼

2. FRONTEND (React)
   │
   ├─→ ChatInput captures text
   ├─→ Calls: chatAPI.sendMessage()
   │
   ▼

3. HTTP REQUEST
   │
   ├─→ POST /api/chat/message
   ├─→ Body: { message: "...", use_documents: true }
   │
   ▼

4. BACKEND RECEIVES
   │
   ├─→ FastAPI endpoint: chat.py
   ├─→ Validates request
   │
   ▼

5. DOCUMENT SEARCH (if use_documents=true)
   │
   ├─→ document_service.search_documents()
   ├─→ Convert question to embedding (OpenAI)
   ├─→ Search FAISS vector store
   ├─→ Return top 3 relevant chunks
   │
   ▼

6. AI PROCESSING
   │
   ├─→ llm_service.chat()
   ├─→ Build prompt with:
   │   • User question
   │   • Document context (if found)
   │   • Conversation history
   ├─→ Send to OpenAI GPT-4
   │
   ▼

7. GPT-4 GENERATES ANSWER
   │
   ├─→ Processes context
   ├─→ Generates natural response
   ├─→ Returns answer
   │
   ▼

8. BACKEND FORMATS RESPONSE
   │
   ├─→ Create ChatResponse object
   ├─→ Add sources (document names)
   ├─→ Return JSON
   │
   ▼

9. FRONTEND DISPLAYS
   │
   ├─→ Updates messages state
   ├─→ Renders ChatMessage component
   ├─→ Shows answer + sources
   │
   ▼

10. USER SEES ANSWER ✅
```

---

## Document Upload Flow

```
1. USER SELECTS FILE
   │
   ├─→ Clicks paperclip icon
   ├─→ Chooses PDF/DOCX/TXT
   │
   ▼

2. FRONTEND PREPARES
   │
   ├─→ Creates FormData
   ├─→ Adds file to form
   │
   ▼

3. HTTP REQUEST
   │
   ├─→ POST /api/documents/upload
   ├─→ Content-Type: multipart/form-data
   │
   ▼

4. BACKEND RECEIVES
   │
   ├─→ documents.py endpoint
   ├─→ Validates file type
   ├─→ Checks file size
   │
   ▼

5. SAVE TO DISK
   │
   ├─→ Save to uploads/ folder
   ├─→ Generate unique ID
   │
   ▼

6. TEXT EXTRACTION
   │
   ├─→ If PDF: PyPDF2.PdfReader
   ├─→ If DOCX: python-docx
   ├─→ If TXT: read directly
   │
   ▼

7. TEXT PROCESSING
   │
   ├─→ Split into chunks (1000 chars)
   ├─→ With 200 char overlap
   ├─→ Using RecursiveCharacterTextSplitter
   │
   ▼

8. GENERATE EMBEDDINGS
   │
   ├─→ For each chunk:
   │   • Send to OpenAI
   │   • Get vector embedding
   │   • Store in memory
   │
   ▼

9. ADD TO VECTOR STORE
   │
   ├─→ Create FAISS index
   ├─→ Add all embeddings
   ├─→ Save to disk (vector_store/)
   │
   ▼

10. RETURN SUCCESS
    │
    ├─→ Send confirmation
    ├─→ Include document info
    ├─→ Frontend shows message
    │
    ▼

11. DOCUMENT READY FOR Q&A ✅
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│            PRESENTATION LAYER               │
│                                             │
│  React Components                           │
│  ├─ App.tsx (Main)                          │
│  ├─ ChatMessage (Display)                   │
│  ├─ ChatInput (User Input)                  │
│  └─ Document List (Sidebar)                 │
│                                             │
│  Styling: Tailwind CSS + shadcn-ui          │
└─────────────────────────────────────────────┘
                    │
                    │ HTTP/REST
                    ▼
┌─────────────────────────────────────────────┐
│             APPLICATION LAYER               │
│                                             │
│  FastAPI Routes                             │
│  ├─ Chat endpoints                          │
│  └─ Document endpoints                      │
│                                             │
│  Business Logic Services                    │
│  ├─ LLM Service (AI)                        │
│  └─ Document Service (Files)                │
└─────────────────────────────────────────────┘
                    │
                    │
                    ▼
┌─────────────────────────────────────────────┐
│               DATA LAYER                    │
│                                             │
│  Vector Storage (FAISS)                     │
│  ├─ Document embeddings                     │
│  └─ Similarity search                       │
│                                             │
│  File Storage                               │
│  ├─ uploads/ (Original files)               │
│  └─ vector_store/ (FAISS index)             │
└─────────────────────────────────────────────┘
                    │
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           EXTERNAL SERVICES                 │
│                                             │
│  OpenAI API                                 │
│  ├─ GPT-4 (Chat completions)                │
│  └─ text-embedding-ada-002 (Embeddings)     │
└─────────────────────────────────────────────┘
```

---

## Key Components Explained

### Frontend (React)

```
App.tsx
├─ State Management
│  ├─ messages (chat history)
│  ├─ documents (uploaded files)
│  ├─ isLoading (loading state)
│  └─ uploadingFile (upload state)
│
├─ Event Handlers
│  ├─ handleSendMessage() → Send to API
│  ├─ handleFileUpload() → Upload document
│  └─ handleDeleteDocument() → Remove file
│
└─ Child Components
   ├─ ChatMessage (displays messages)
   ├─ ChatInput (user input)
   └─ Document List (sidebar)
```

### Backend (FastAPI)

```
main.py
└─ FastAPI App
   ├─ CORS middleware
   ├─ Route includes
   │  ├─ /api/chat/*
   │  └─ /api/documents/*
   └─ Static file serving

Services Layer
├─ LLM Service
│  ├─ OpenAI client
│  ├─ chat() method
│  └─ prompt engineering
│
└─ Document Service
   ├─ File processing
   ├─ Text extraction
   ├─ FAISS indexing
   └─ Similarity search
```

---

## Security & Best Practices

```
✅ Environment Variables
   ├─ API keys in .env
   ├─ Not committed to git
   └─ Different for dev/prod

✅ Input Validation
   ├─ File type checking
   ├─ File size limits
   └─ Request validation (Pydantic)

✅ Error Handling
   ├─ Try-catch blocks
   ├─ Meaningful error messages
   └─ Logging

✅ CORS Configuration
   ├─ Allowed origins
   └─ Credentials handling
```

---

## Performance Optimizations

```
⚡ Frontend
   ├─ React.memo for components
   ├─ Lazy loading
   └─ Efficient re-renders

⚡ Backend
   ├─ FAISS (fast search)
   ├─ Chunking strategy
   └─ Async operations

⚡ API
   ├─ Streaming responses
   ├─ Compression
   └─ Caching (future)
```

---

## Deployment Architecture (Future)

```
┌────────────────────────────────────┐
│   CDN (Cloudflare/CloudFront)     │
│         Static Assets               │
└────────────┬───────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│    Frontend (Vercel/Netlify)       │
│    - React Build                    │
│    - Static Hosting                 │
└────────────┬───────────────────────┘
             │
             │ HTTPS
             ▼
┌────────────────────────────────────┐
│    Backend (Railway/Render)        │
│    - FastAPI Server                 │
│    - Container Deployment           │
└────────────┬───────────────────────┘
             │
             ├─→ OpenAI API
             │
             └─→ Persistent Storage
                 (PostgreSQL/S3)
```

---

## Monitoring & Logging (Future Enhancement)

```
📊 Metrics to Track
   ├─ Request count
   ├─ Response time
   ├─ Error rate
   ├─ OpenAI API usage
   └─ Document count

📝 Logging Strategy
   ├─ Request/Response logs
   ├─ Error logs
   ├─ Performance logs
   └─ User activity logs
```

---

This architecture is:
✅ **Scalable** - Can handle more users
✅ **Maintainable** - Clean separation of concerns
✅ **Testable** - Each component is independent
✅ **Resume-worthy** - Industry-standard patterns
