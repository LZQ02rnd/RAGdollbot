# RAGdollBot Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Discord Server                        │
│                                                              │
│  User: "!ask When are the meetings?"                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                        bot.py                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Discord Bot (discord.py)                           │   │
│  │  - Receives commands                                │   │
│  │  - Parses user input                                │   │
│  │  - Formats responses                                │   │
│  └──────────────┬──────────────────────────────────────┘   │
└─────────────────┼───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      rag_engine.py                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RAG Engine                                         │   │
│  │                                                     │   │
│  │  1. Receives question                              │   │
│  │  2. Creates embedding of question                  │   │
│  │  3. Searches vector store for similar chunks       │   │
│  │  4. Retrieves top K relevant documents             │   │
│  │  5. Combines context + question                    │   │
│  │  6. Sends to LLM                                   │   │
│  │  7. Returns answer + sources                       │   │
│  └──────────────┬──────────────────────────────────────┘   │
└─────────────────┼───────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────┬────────────────────────────┐
│                                │                            │
│    Vector Store (ChromaDB)     │     OpenAI API             │
│                                │                            │
│  ┌──────────────────────┐     │  ┌──────────────────────┐  │
│  │ Document Embeddings  │     │  │ Embeddings (text-    │  │
│  │                      │     │  │ embedding-ada-002)   │  │
│  │ [0.1, 0.5, ...]     │     │  │                      │  │
│  │ [0.3, 0.2, ...]     │◄────┼──┤ LLM (gpt-3.5-turbo) │  │
│  │ [0.8, 0.1, ...]     │     │  │                      │  │
│  │       ...            │     │  │ Generates answers    │  │
│  └──────────────────────┘     │  └──────────────────────┘  │
│                                │                            │
└────────────────────────────────┴────────────────────────────┘
                  ▲
                  │
                  │ Initial Load
                  │
┌─────────────────────────────────────────────────────────────┐
│                    knowledge_base/                           │
│                                                              │
│  club_info.txt        resources.txt        [your docs]      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Meeting info │    │ Scholarships │    │ Custom docs  │  │
│  │ Contact info │    │ Resources    │    │ PDFs, etc.   │  │
│  │ FAQ          │    │ Alumni info  │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initialization (Bot Startup)
```
knowledge_base/ → Load Documents → Split into Chunks → 
Create Embeddings → Store in ChromaDB
```

### 2. Question Answering
```
User Question → Discord Bot → RAG Engine →
├─ Create Question Embedding (OpenAI)
├─ Search Vector Store (ChromaDB)
├─ Retrieve Top K Documents
├─ Combine Context + Question
├─ Send to LLM (OpenAI)
└─ Return Answer + Sources → Format Response → Send to Discord
```

## Component Details

### bot.py
- **Purpose**: Discord interface
- **Dependencies**: discord.py, rag_engine
- **Commands**: 
  - `!ask` - Ask a question
  - `!info` - Bot information
  - `!reload` - Reload knowledge base (admin)
  - `!ping` - Check latency
  - `!help` - Show help

### rag_engine.py
- **Purpose**: RAG logic and document processing
- **Dependencies**: langchain, openai, chromadb
- **Key Methods**:
  - `load_documents()` - Load from knowledge_base/
  - `split_documents()` - Chunk documents
  - `initialize_vector_store()` - Create/load vector DB
  - `answer_question()` - RAG pipeline

### config.py
- **Purpose**: Configuration management
- **Source**: Environment variables (.env)
- **Settings**: Tokens, API keys, model parameters

## Configuration Flow

```
.env.example → User copies to .env → Fills in secrets →
config.py loads → Provides to bot.py and rag_engine.py
```

## Security Model

```
┌─────────────────────────────────────────┐
│  Secrets (.env)                         │
│  - DISCORD_BOT_TOKEN                    │
│  - OPENAI_API_KEY                       │
│  [gitignored, never committed]          │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  config.py                              │
│  - Loads from environment               │
│  - Validates required values            │
│  - No hardcoded secrets                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Runtime (bot.py, rag_engine.py)        │
│  - Uses config values                   │
│  - Never logs/exposes secrets           │
└─────────────────────────────────────────┘
```

## Deployment Options

### Option 1: Local Development
```
Laptop/Desktop → Python venv → Run bot.py
↓
Works while computer is on
```

### Option 2: Cloud Server (Recommended for 24/7)
```
AWS/GCP/DigitalOcean → Ubuntu VM → systemd service
↓
Always running, auto-restart on failure
```

### Option 3: Docker (Advanced)
```
Dockerfile → Docker image → Docker container
↓
Portable, isolated environment
```

## Scaling Considerations

### Small Club (< 100 members)
- Single instance
- GPT-3.5-turbo
- Basic knowledge base

### Medium Club (100-500 members)
- Single instance with caching
- Consider rate limiting
- Organized knowledge base

### Large Club (500+ members)
- Load balancer
- Multiple bot instances
- Distributed vector store
- GPT-4 for better quality
- Usage monitoring/analytics

## Extension Points

1. **Custom Commands**: Add to `bot.py`
2. **Document Types**: Extend loaders in `rag_engine.py`
3. **Vector Stores**: Swap ChromaDB for Pinecone/Weaviate
4. **LLM Models**: Change in config (GPT-4, Claude, etc.)
5. **Embeddings**: Different embedding models
6. **UI**: Add web dashboard
7. **Analytics**: Track usage patterns
8. **Multi-language**: Add translation layer

## Technology Stack

- **Python 3.8+**: Programming language
- **discord.py**: Discord API wrapper
- **LangChain**: RAG framework
- **OpenAI**: Embeddings + LLM
- **ChromaDB**: Vector database
- **python-dotenv**: Environment config
