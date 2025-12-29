"""Discord bot for RAG-based club information."""
import discord
from discord.ext import commands
from config import Config
from rag_system import RAGSystem
import asyncio

# Validate configuration
Config.validate()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
# intents.members = True  # Optional - only needed for member-related features

bot = commands.Bot(command_prefix=Config.BOT_PREFIX, intents=intents)

# Initialize RAG system
rag = RAGSystem()


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Auto-load knowledge base if it doesn't exist
    try:
        # Check if knowledge base collection exists and has data
        try:
            collection = rag.client.get_collection(name="club_knowledge")
            count = collection.count()
            if count == 0:
                print("Knowledge base is empty, loading from files...")
                from knowledge_loader import load_knowledge_base
                load_knowledge_base(rag)
                # Re-initialize vectorstore after loading
                rag.vectorstore = Chroma(
                    client=rag.client,
                    collection_name="club_knowledge",
                    embedding_function=rag.embeddings
                )
                # Re-create QA chain with new vectorstore
                from langchain_core.runnables import RunnablePassthrough
                from langchain_core.output_parsers import StrOutputParser
                retriever = rag.vectorstore.as_retriever(search_kwargs={"k": 4})
                def format_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)
                rag.qa_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | rag.prompt_template
                    | rag.llm
                    | StrOutputParser()
                )
                print("Knowledge base loaded successfully!")
            else:
                print(f"Knowledge base already loaded ({count} chunks)")
        except Exception as e:
            # Collection doesn't exist, create and load it
            print(f"Knowledge base collection not found ({e}), creating and loading...")
            from knowledge_loader import load_knowledge_base
            load_knowledge_base(rag)
            # Re-initialize vectorstore after loading
            from langchain_community.vectorstores import Chroma
            from langchain_core.runnables import RunnablePassthrough
            from langchain_core.output_parsers import StrOutputParser
            rag.vectorstore = Chroma(
                client=rag.client,
                collection_name="club_knowledge",
                embedding_function=rag.embeddings
            )
            # Re-create QA chain
            retriever = rag.vectorstore.as_retriever(search_kwargs={"k": 4})
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            rag.qa_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | rag.prompt_template
                | rag.llm
                | StrOutputParser()
            )
            print("Knowledge base loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not auto-load knowledge base: {e}")
        print("Use !reload_kb command to load it manually.")
        import traceback
        traceback.print_exc()
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{Config.BOT_PREFIX}help"
        )
    )


@bot.event
async def on_message(message):
    """Handle incoming messages."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if message mentions the bot or starts with prefix
    bot_mentioned = bot.user in message.mentions
    is_command = message.content.startswith(Config.BOT_PREFIX)
    
    # If it's a command, process commands first
    if is_command:
        # Check if it's a known command (let commands.py handle it)
        ctx = await bot.get_context(message)
        if ctx.command is not None:
            # It's a valid command, let the command handler process it
            await bot.process_commands(message)
            return
    
    # If bot is mentioned or message starts with prefix (but not a command), treat as query
    if bot_mentioned or (is_command and not ctx.command):
        # Remove mention and prefix for processing
        query = message.content
        if bot_mentioned:
            # Remove bot mention
            query = query.replace(f"<@{bot.user.id}>", "").strip()
        if is_command:
            # Remove prefix
            query = query[len(Config.BOT_PREFIX):].strip()
        
        # If there's a query, process it
        if query:
            # Show typing indicator
            async with message.channel.typing():
                try:
                    # Get answer from RAG system
                    answer = rag.query(query)
                    
                    # Send response
                    await message.reply(answer)
                except Exception as e:
                    await message.reply(f"Sorry, I encountered an error: {str(e)}")
            return
    
    # Process any remaining commands
    await bot.process_commands(message)


@bot.command(name='info', aliases=['h', 'about'])
async def info_command(ctx):
    """Display help information."""
    help_text = f"""
**RAGdollbot Help**

I'm a RAG (Retrieval-Augmented Generation) bot that can answer questions about the club!

**How to use:**
- Mention me (@{bot.user.name}) followed by your question
- Or use `{Config.BOT_PREFIX}ask <question>` command

**Commands:**
- `{Config.BOT_PREFIX}info` - Show this help message
- `{Config.BOT_PREFIX}ask <question>` - Ask a question about the club
- `{Config.BOT_PREFIX}ping` - Check if the bot is online

**Example:**
@{bot.user.name} What are the meeting times?
or
{Config.BOT_PREFIX}ask What are the meeting times?
"""
    await ctx.send(help_text)


@bot.command(name='ask')
async def ask_command(ctx, *, question: str):
    """Ask a question about the club."""
    if not question:
        await ctx.send("Please provide a question! Use `!ask <your question>`")
        return
    
    async with ctx.channel.typing():
        try:
            answer = rag.query(question)
            await ctx.reply(answer)
        except Exception as e:
            await ctx.reply(f"Sorry, I encountered an error: {str(e)}")


@bot.command(name='ping')
async def ping_command(ctx):
    """Check bot latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")


@bot.command(name='reload_kb')
@commands.has_permissions(administrator=True)
async def reload_knowledge_base(ctx):
    """Reload the knowledge base from files (admin only)."""
    await ctx.send("Reloading knowledge base...")
    try:
        from knowledge_loader import load_knowledge_base
        load_knowledge_base(rag)
        await ctx.send("✅ Knowledge base reloaded successfully!")
    except Exception as e:
        await ctx.send(f"❌ Error reloading knowledge base: {str(e)}")


@bot.command(name='clear_kb')
@commands.has_permissions(administrator=True)
async def clear_knowledge_base(ctx):
    """Clear the knowledge base (admin only)."""
    rag.clear_knowledge_base()
    await ctx.send("✅ Knowledge base cleared!")


@reload_knowledge_base.error
@clear_knowledge_base.error
async def admin_error(ctx, error):
    """Handle permission errors for admin commands."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")


def main():
    """Run the bot."""
    try:
        bot.run(Config.DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Make sure your .env file is configured correctly!")


if __name__ == "__main__":
    main()

