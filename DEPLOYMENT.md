# Deployment Checklist

Use this checklist to deploy RAGdollBot to your Discord server.

## Pre-Deployment

### 1. Get API Keys
- [ ] Create Discord application at https://discord.com/developers/applications
- [ ] Create Discord bot and copy token
- [ ] Enable "Message Content Intent" in Discord bot settings
- [ ] Create OpenAI account at https://platform.openai.com
- [ ] Generate OpenAI API key
- [ ] Add credits to OpenAI account (minimum $5 recommended)

### 2. Prepare Environment
- [ ] Install Python 3.8+ on your system
- [ ] Clone the RAGdollBot repository
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`

### 3. Configure Bot
- [ ] Copy `.env.example` to `.env`
- [ ] Add Discord bot token to `.env`
- [ ] Add OpenAI API key to `.env`
- [ ] Review and adjust other settings (optional)

### 4. Prepare Knowledge Base
- [ ] Add your club's documents to `knowledge_base/` folder
- [ ] Supported formats: `.txt`, `.pdf`
- [ ] Organize documents logically (optional subdirectories supported)
- [ ] Remove example documents if not needed

## Deployment

### 5. Test Locally
- [ ] Run verification: `python setup.py`
- [ ] Fix any issues reported
- [ ] Start bot: `python bot.py`
- [ ] Verify bot comes online successfully
- [ ] Check console for any errors

### 6. Invite Bot to Server
- [ ] Go to Discord Developer Portal → OAuth2 → URL Generator
- [ ] Select scopes: `bot`, `applications.commands`
- [ ] Select permissions: Send Messages, Read Messages, Embed Links, Read Message History
- [ ] Copy generated URL
- [ ] Open URL in browser
- [ ] Select your server
- [ ] Authorize bot

### 7. Test Commands
- [ ] Test `!ping` - should respond with latency
- [ ] Test `!info` - should show bot information
- [ ] Test `!ask <question>` - should answer based on knowledge base
- [ ] Test `!help` - should show all commands
- [ ] Test `!reload` (as admin) - should reload knowledge base

## Post-Deployment

### 8. Monitor and Maintain
- [ ] Monitor console for errors
- [ ] Check bot responses are accurate
- [ ] Update knowledge base as needed
- [ ] Run `!reload` after updating documents

### 9. User Training
- [ ] Share command list with club members
- [ ] Explain how to ask questions effectively
- [ ] Designate administrators who can use `!reload`
- [ ] Create channel guidelines for bot usage

### 10. Production Considerations (Optional)

For 24/7 uptime:
- [ ] Set up dedicated server (VPS, cloud instance)
- [ ] Configure bot to run as a service (systemd, pm2, etc.)
- [ ] Set up logging
- [ ] Configure automatic restarts on failure
- [ ] Set up monitoring/alerts

Example systemd service file:
```ini
[Unit]
Description=RAGdollBot Discord Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/RAGdollbot
Environment=PATH=/path/to/RAGdollbot/venv/bin
ExecStart=/path/to/RAGdollbot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Troubleshooting Reference

### Bot won't start
1. Check `.env` file exists and has correct values
2. Verify virtual environment is activated
3. Ensure all dependencies are installed
4. Check Python version is 3.8+

### Bot is online but doesn't respond
1. Verify bot has proper permissions in Discord
2. Check "Message Content Intent" is enabled
3. Ensure bot can see the channel
4. Check console for errors

### "Knowledge base not initialized" error
1. Add documents to `knowledge_base/` folder
2. Restart bot to re-initialize
3. Use `!reload` command (admin only)
4. Check console for document loading errors

### Slow responses
1. Reduce `TOP_K_RESULTS` in `.env` (try 2-3)
2. Reduce `CHUNK_SIZE` if documents are very large
3. Check OpenAI API rate limits
4. Consider upgrading to GPT-4 for better quality

### High costs
1. Monitor OpenAI API usage dashboard
2. Use GPT-3.5-turbo instead of GPT-4 (default)
3. Reduce `TOP_K_RESULTS` to minimize context size
4. Set usage limits in OpenAI account

## Security Checklist

- [ ] `.env` file is not committed to git (in `.gitignore`)
- [ ] API keys are not shared publicly
- [ ] Bot permissions are minimal (only what's needed)
- [ ] Admin commands are properly restricted
- [ ] Regular updates to dependencies for security patches

## Maintenance Schedule

Recommended schedule:
- **Daily**: Monitor console for errors
- **Weekly**: Check bot responses are accurate
- **Monthly**: Update knowledge base with new information
- **Quarterly**: Update dependencies: `pip install -r requirements.txt --upgrade`

## Support

If you encounter issues:
1. Check the [README.md](README.md) troubleshooting section
2. Review console logs for errors
3. Verify all checklist items are completed
4. Open an issue on GitHub with details

---

✅ Deployment Complete! Your RAG Discord bot is ready to serve your university club!
