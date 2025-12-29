# RAGdollbot

A Discord bot powered by RAG (Retrieval-Augmented Generation) that answers questions about your university club or any community server using a knowledge base.

**Currently used by [McGill Esports Association](https://www.mcgillesports.ca/)**

## Features

- 🤖 **Intelligent Q&A**: Users can now ask questions about your club and get accurate answers based on your knowledge base instead of @Admins 24/7
- 📚 **Knowledge Base**: Easy-to-manage text-based knowledge base! Type in any info you want.
- 🔍 **Semantic Search**: Uses embeddings to find the most relevant information
- 💬 **Discord Integration**: Works seamlessly in Discord servers
- ⚙️ **Admin Commands**: Manage and reload the knowledge base from Discord. 

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([How to create a Discord bot](https://discord.com/developers/applications))
- **Free LLM Options:**
  - **Groq API Key** (Recommended - FREE, no credit card needed) - [Get one here](https://console.groq.com/keys)
  - **Ollama** (FREE, local) - [Install from here](https://ollama.ai)
  - Optional: DeepSeek or OpenAI API Key (paid alternatives)

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
     ```
     DISCORD_BOT_TOKEN=your_discord_bot_token_here
     LLM_PROVIDER=groq
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - **For FREE setup:** Get a Groq API key at [console.groq.com/keys](https://console.groq.com/keys) (free, no credit card needed)
   - Note: Embeddings use free local models by default (sentence-transformers). To use OpenAI embeddings instead, set `USE_OPENAI_EMBEDDINGS=true` and add your `OPENAI_API_KEY`.

4. **Add your club information**
   - Add `.txt` files to the `knowledge_base/` directory with your club information
   - See `knowledge_base/README.md` for more details

5. **Index the knowledge base**
   ```bash
   python knowledge_loader.py
   ```

6. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

### In Discord

**Ask questions:**
- Mention the bot: `@RAGdollbot What are the meeting times?`
- Use the command: `!ask What are the meeting times?`

**Commands:**
- `!info` or `!h` - Show help information
- `!ask <question>` - Ask a question about the club
- `!ping` - Check bot latency
- `!reload_kb` - Reload knowledge base (admin only)
- `!clear_kb` - Clear knowledge base (admin only)

### Updating the Knowledge Base

1. Add or edit `.txt` files in the `knowledge_base/` directory
2. Run `python knowledge_loader.py` to re-index
3. Or use `!reload_kb` command in Discord (requires admin permissions)

## Configuration

Edit `.env` file to customize:

- `DISCORD_BOT_TOKEN` - Your Discord bot token (required)
- `LLM_PROVIDER` - LLM provider: `groq` (free), `ollama` (free local), `deepseek`, or `openai` (default: `groq`)
- `GROQ_API_KEY` - Your Groq API key (required if `LLM_PROVIDER=groq`) - [Get free key](https://console.groq.com/keys)
- `GROQ_MODEL` - Groq model to use (default: `llama-3.1-8b-instant`)
- `OLLAMA_BASE_URL` - Ollama API URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL` - Ollama model name (default: `llama3.2`)
- `DEEPSEEK_API_KEY` - DeepSeek API key (only if `LLM_PROVIDER=deepseek`)
- `OPENAI_API_KEY` - OpenAI API key (only if `LLM_PROVIDER=openai`)
- `EMBEDDING_MODEL` - Embedding model (default: `all-MiniLM-L6-v2` for free local embeddings)
- `USE_OPENAI_EMBEDDINGS` - Use OpenAI embeddings instead (default: `false`)
- `BOT_PREFIX` - Command prefix (default: `!`)
- `MAX_MESSAGE_LENGTH` - Maximum response length (default: 2000)

## 24/7 Hosting on Railway (Recommended)

Deploy your bot to Railway for free 24/7 hosting:

1. **Push to GitHub** (if not already done)
2. **Sign up at [Railway.app](https://railway.app)** (free tier available)
3. **Create New Project** → Deploy from GitHub repo
4. **Add Environment Variables** in Railway's Variables tab:
   - `DISCORD_BOT_TOKEN` - Your Discord bot token
   - `LLM_PROVIDER=groq`
   - `GROQ_API_KEY` - Your Groq API key
   - `GROQ_MODEL=llama-3.1-8b-instant` (optional)
5. **Deploy** - Railway will automatically build and deploy
6. **Done!** Your bot runs 24/7

See `RAILWAY_DEPLOY.md` for detailed instructions.

## Project Structure

```
RAGdollbot/
├── bot.py                 # Main Discord bot
├── rag_system.py          # RAG implementation
├── knowledge_loader.py    # Knowledge base loader
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration for Railway
├── Procfile               # Process file for Railway
├── .env.example           # Environment variables template
├── knowledge_base/        # Club information files
│   └── *.txt             # Your club information
└── chroma_db/            # Vector database (auto-created)
```

## How It Works

1. **Knowledge Base**: Text files in `knowledge_base/` are split into chunks and embedded using free local models (sentence-transformers)
2. **Vector Store**: Embeddings are stored in ChromaDB for fast similarity search
3. **Query Processing**: When a user asks a question:
   - The question is embedded
   - Similar chunks are retrieved from the knowledge base
   - A free LLM (Groq) generates an answer based on the retrieved context
4. **Response**: The bot sends the generated answer to Discord

## Free LLM Options

This bot is designed to run **completely free**:

- **Groq** (Recommended): Free API, fast responses, no credit card needed
- **Ollama**: Free local LLM, runs on your machine (or Railway)
- **Embeddings**: Free local models (sentence-transformers) - no API costs

No paid services required!

## Troubleshooting

**Bot doesn't respond:**
- Check that the bot token is correct in `.env`
- Ensure the bot has proper permissions in your Discord server
- Verify the bot is online (check console output)

**Answers are inaccurate:**
- Make sure your knowledge base files contain relevant information
- Try re-indexing with `python knowledge_loader.py`
- Check that the question is related to your knowledge base content

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## License

MIT License - see LICENSE file for details

## Contributing

Feel free to submit issues or pull requests!
