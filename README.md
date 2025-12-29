# RAGdollbot

A Discord bot powered by RAG (Retrieval-Augmented Generation) that answers questions about your university club using a knowledge base.

## Features

- 🤖 **Intelligent Q&A**: Ask questions about your club and get accurate answers based on your knowledge base
- 📚 **Knowledge Base**: Easy-to-manage text-based knowledge base
- 🔍 **Semantic Search**: Uses embeddings to find the most relevant information
- 💬 **Discord Integration**: Works seamlessly in Discord servers
- ⚙️ **Admin Commands**: Manage and reload the knowledge base from Discord

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([How to create a Discord bot](https://discord.com/developers/applications))
- DeepSeek API Key ([Get one here](https://platform.deepseek.com/api_keys))
  - Optional: OpenAI API Key (only if you want to use OpenAI embeddings instead of free local embeddings)

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
     DEEPSEEK_API_KEY=your_deepseek_api_key_here
     ```
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
- `!help` - Show help information
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
- `DEEPSEEK_API_KEY` - Your DeepSeek API key (required)
- `DEEPSEEK_API_BASE` - DeepSeek API endpoint (default: `https://api.deepseek.com`)
- `DEEPSEEK_MODEL` - DeepSeek model to use (default: `deepseek-chat`)
- `EMBEDDING_MODEL` - Embedding model (default: `all-MiniLM-L6-v2` for free local embeddings)
- `USE_OPENAI_EMBEDDINGS` - Use OpenAI embeddings instead (default: `false`)
- `OPENAI_API_KEY` - OpenAI API key (only needed if `USE_OPENAI_EMBEDDINGS=true`)
- `BOT_PREFIX` - Command prefix (default: `!`)
- `MAX_MESSAGE_LENGTH` - Maximum response length (default: 2000)

## Project Structure

```
RAGdollbot/
├── bot.py                 # Main Discord bot
├── rag_system.py          # RAG implementation
├── knowledge_loader.py    # Knowledge base loader
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── knowledge_base/        # Club information files
│   └── *.txt             # Your club information
└── chroma_db/            # Vector database (auto-created)
```

## How It Works

1. **Knowledge Base**: Text files in `knowledge_base/` are split into chunks and embedded
2. **Vector Store**: Embeddings are stored in ChromaDB for fast similarity search
3. **Query Processing**: When a user asks a question:
   - The question is embedded
   - Similar chunks are retrieved from the knowledge base
   - An LLM generates an answer based on the retrieved context
4. **Response**: The bot sends the generated answer to Discord

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
