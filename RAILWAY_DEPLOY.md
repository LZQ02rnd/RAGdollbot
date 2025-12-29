# Railway Deployment Guide

Follow these steps to deploy your Discord RAG bot to Railway for 24/7 hosting.

## Prerequisites
- GitHub account
- Railway account (free at https://railway.app)

## Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Discord RAG bot"
   ```

2. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (make it private if you want)
   - Don't initialize with README

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Railway

1. **Sign up/Login to Railway**:
   - Go to https://railway.app
   - Sign up with GitHub (free)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect Python

3. **Add Environment Variables**:
   - Click on your project
   - Go to "Variables" tab
   - Add these variables:
     ```
     DISCORD_BOT_TOKEN=your_discord_bot_token
     LLM_PROVIDER=groq
     GROQ_API_KEY=your_groq_api_key
     GROQ_MODEL=llama-3.1-8b-instant
     EMBEDDING_MODEL=all-MiniLM-L6-v2
     USE_OPENAI_EMBEDDINGS=false
     CHROMA_PERSIST_DIRECTORY=./chroma_db
     BOT_PREFIX=!
     MAX_MESSAGE_LENGTH=2000
     ```

4. **Deploy**:
   - Railway will automatically start deploying
   - Watch the logs to see if it starts successfully
   - The bot should connect to Discord when ready

## Step 3: Verify Deployment

1. **Check Logs**:
   - In Railway dashboard, click on your service
   - Go to "Logs" tab
   - You should see: `[BotName] has connected to Discord!`

2. **Test in Discord**:
   - Check if bot is online in your server
   - Try: `!help` or `@BotName test`

## Important Notes

- **Free Tier Limits**: Railway free tier gives you $5 credit/month
- **Sleeping**: Free tier may sleep after inactivity (paid plans don't)
- **Storage**: ChromaDB data persists in Railway's filesystem
- **Updates**: Push to GitHub to automatically redeploy

## Troubleshooting

**Bot not connecting?**
- Check logs in Railway dashboard
- Verify Discord token is correct
- Ensure bot has proper permissions in Discord server

**Build fails?**
- Check that all dependencies are in requirements.txt
- Verify Python version compatibility

**Need to update?**
- Make changes locally
- Commit and push to GitHub
- Railway auto-deploys on push

## Cost

- **Free tier**: $5 credit/month (enough for a RAGdollbot)
- **Hobby plan**: $20/month (more resources)

RAGdollbot will now run 24/7! 🚀

