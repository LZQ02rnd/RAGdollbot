# Quick Start Guide

This guide will help you get RAGdollBot up and running in under 10 minutes!

## Step 1: Prerequisites

Make sure you have:
- Python 3.8+ installed
- A Discord account
- An OpenAI account with API access

## Step 2: Get Your API Keys

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot" → "Yes, do it!"
5. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
6. Click "Reset Token" and copy the token (save it somewhere safe!)

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (save it somewhere safe!)
4. Note: You'll need to add credits to your OpenAI account

## Step 3: Install RAGdollBot

```bash
# Clone the repository
git clone https://github.com/LZQ02rnd/RAGdollbot.git
cd RAGdollbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Configure the Bot

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite text editor
# Add your Discord Bot Token and OpenAI API Key
nano .env  # or vim, code, notepad, etc.
```

Your `.env` should look like:
```
DISCORD_BOT_TOKEN=your_actual_discord_token_here
OPENAI_API_KEY=sk-your_actual_openai_key_here
```

## Step 5: Add Knowledge Base Documents

Place your club's documents in the `knowledge_base/` folder:

```bash
# Example documents are already included!
# Add your own .txt or .pdf files:
cp /path/to/your/club_handbook.pdf knowledge_base/
cp /path/to/your/faq.txt knowledge_base/
```

## Step 6: Invite Bot to Your Server

1. Go back to https://discord.com/developers/applications
2. Select your application
3. Go to "OAuth2" → "URL Generator"
4. Select scopes:
   - ✅ bot
   - ✅ applications.commands
5. Select permissions:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Embed Links
   - ✅ Read Message History
6. Copy the generated URL and open it in your browser
7. Select your server and authorize the bot

## Step 7: Start the Bot

```bash
# Run the setup verification (optional but recommended)
python setup.py

# Start the bot
python bot.py
```

You should see:
```
Initializing RAG engine...
Loading existing vector store...
RAG engine initialized!
RAGdollBot#1234 has connected to Discord!
Bot is in 1 guilds
```

## Step 8: Test It Out!

In your Discord server, try:

```
!ping
!info
!ask When are the club meetings?
!ask How do I become a member?
```

## Troubleshooting

### Bot doesn't appear online
- Check your Discord Bot Token in `.env`
- Make sure you invited the bot to your server
- Verify the bot has proper permissions

### "OPENAI_API_KEY is required" error
- Check your OpenAI API Key in `.env`
- Make sure the key starts with `sk-`

### ModuleNotFoundError
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Bot responds with "knowledge base is not initialized"
- Make sure you have documents in `knowledge_base/`
- Wait for the bot to fully start (check console output)
- Try the `!reload` command (requires admin permissions)

## Next Steps

1. **Customize Your Knowledge Base**: Add your club's specific documents
2. **Adjust Settings**: Edit `.env` to fine-tune bot behavior
3. **Train Your Members**: Share the `!help` command with your club
4. **Monitor Usage**: Watch the console for errors or issues

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the [Troubleshooting section](README.md#troubleshooting)
- Open an issue on GitHub

---

Congrats! Your RAG Discord bot is now running! 🎉
