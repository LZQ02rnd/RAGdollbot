# RAGdollbot 🤖

A Retrieval-Augmented Generation (RAG) powered Discord bot designed to answer questions for university club members using a custom knowledge base.

## Features

- 🔍 **Smart Question Answering**: Uses RAG to provide accurate answers based on your club's knowledge base
- 📚 **Document Support**: Supports both text (.txt) and PDF (.pdf) documents
- 🎯 **Context-Aware**: Retrieves relevant information from documents to answer questions
- 🔄 **Easy Updates**: Reload knowledge base without restarting the bot
- 💬 **Discord Integration**: Simple commands for seamless Discord interaction
- 🎨 **Rich Embeds**: Beautiful formatted responses with source citations

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([How to get one](https://discord.com/developers/applications))
- OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LZQ02rnd/RAGdollbot.git
   cd RAGdollbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your tokens:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Add your knowledge base documents**
   
   Place your club's documents (text files or PDFs) in the `knowledge_base/` directory. The bot will automatically process these documents when it starts.

6. **Run the bot**
   ```bash
   python bot.py
   ```

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Enable the following Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent (optional)
5. Copy the bot token to your `.env` file
6. Go to OAuth2 → URL Generator
7. Select scopes: `bot`, `applications.commands`
8. Select bot permissions: `Send Messages`, `Read Messages/View Channels`, `Embed Links`, `Read Message History`
9. Use the generated URL to invite the bot to your server

## Usage

### Commands

- **`!ask <question>`** - Ask a question to the bot
  ```
  !ask When are the club meetings?
  !ask How do I become a member?
  !ask What scholarships are available?
  ```

- **`!info`** - Get information about the bot
  ```
  !info
  ```

- **`!ping`** - Check if the bot is responsive
  ```
  !ping
  ```

- **`!reload`** - Reload the knowledge base (requires administrator permissions)
  ```
  !reload
  ```

- **`!help`** - Show all available commands
  ```
  !help
  ```

### Example Interaction

```
User: !ask When are the meetings?
Bot: 🤖 Answer
Regular meetings are held every Wednesday at 5:00 PM in Room 204, Student Center. Board meetings are on the first Monday of each month at 6:00 PM.

❓ Question: When are the meetings?
📚 Sources: club_info.txt
```

## Configuration

You can customize the bot's behavior by editing the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | Required |
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `COMMAND_PREFIX` | Bot command prefix | `!` |
| `BOT_NAME` | Bot display name | `RAGdollBot` |
| `MODEL_NAME` | OpenAI model to use | `gpt-3.5-turbo` |
| `TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `CHUNK_SIZE` | Document chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap size | `200` |
| `TOP_K_RESULTS` | Number of results to retrieve | `3` |

## Project Structure

```
RAGdollbot/
├── bot.py                 # Main Discord bot implementation
├── rag_engine.py          # RAG engine for document processing and QA
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── knowledge_base/       # Directory for club documents
│   ├── club_info.txt     # Example: General club information
│   └── resources.txt     # Example: Resources and opportunities
├── vector_store/         # Vector database (auto-generated)
└── README.md            # This file
```

## How It Works

1. **Document Ingestion**: The bot loads all documents from the `knowledge_base/` directory
2. **Text Splitting**: Documents are split into manageable chunks with overlap
3. **Embedding**: Text chunks are converted to vector embeddings using OpenAI
4. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
5. **Question Processing**: When a user asks a question:
   - The question is converted to an embedding
   - Similar document chunks are retrieved from the vector store
   - The relevant context and question are sent to the LLM
   - The LLM generates a coherent answer based on the context
6. **Response**: The answer is formatted and sent back to Discord with source citations

## Adding New Documents

1. Add your documents (`.txt` or `.pdf` files) to the `knowledge_base/` directory
2. Use the `!reload` command in Discord (requires admin permissions)
3. The bot will process and index the new documents

## Troubleshooting

### Bot doesn't respond
- Check if the bot is online in Discord
- Verify the bot has proper permissions in your server
- Check the console for error messages

### "DISCORD_BOT_TOKEN is required" error
- Make sure you've created a `.env` file
- Verify the token is correctly copied from Discord Developer Portal

### "No documents found" warning
- Add documents to the `knowledge_base/` directory
- Supported formats: `.txt` and `.pdf`

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

## Technology Stack

- **Discord.py**: Discord bot framework
- **LangChain**: RAG orchestration and document processing
- **OpenAI**: Language model and embeddings
- **ChromaDB**: Vector database for document storage
- **Python-dotenv**: Environment variable management

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or issues:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the configuration options

## Acknowledgments

- Built with LangChain for RAG capabilities
- Powered by OpenAI's GPT models
- Uses ChromaDB for efficient vector storage

---

Made with ❤️ for university clubs