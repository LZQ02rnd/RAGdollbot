"""
Discord bot for RAGdollBot - A RAG-powered Q&A bot for university clubs
"""
import discord
from discord.ext import commands
import asyncio
from typing import Optional
from config import Config
from rag_engine import RAGEngine


class RAGdollBot(commands.Bot):
    """Discord bot with RAG capabilities"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
        
        self.rag_engine: Optional[RAGEngine] = None
        
    async def setup_hook(self):
        """Initialize the bot"""
        print("Initializing RAG engine...")
        self.rag_engine = RAGEngine()
        
        # Initialize vector store in a separate thread to avoid blocking
        await asyncio.to_thread(self.rag_engine.initialize_vector_store)
        print("RAG engine initialized!")
        
    async def on_ready(self):
        """Called when bot is ready"""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{Config.COMMAND_PREFIX}ask | {Config.COMMAND_PREFIX}help"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Process commands
        await self.process_commands(message)


def setup_bot():
    """Set up and configure the bot with commands"""
    bot = RAGdollBot()
    
    @bot.command(name='ask', help='Ask a question to the bot')
    async def ask(ctx, *, question: str):
        """Ask a question and get an answer from the knowledge base"""
        async with ctx.typing():
            # Run RAG query in a separate thread to avoid blocking
            result = await asyncio.to_thread(
                bot.rag_engine.answer_question,
                question
            )
        
        # Create embed for better formatting
        embed = discord.Embed(
            title="🤖 Answer",
            description=result["answer"],
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="❓ Question",
            value=question,
            inline=False
        )
        
        if result["sources"]:
            sources_text = "\n".join([f"• {source}" for source in result["sources"]])
            embed.add_field(
                name="📚 Sources",
                value=sources_text,
                inline=False
            )
        
        embed.set_footer(text=f"Asked by {ctx.author.name}")
        
        await ctx.reply(embed=embed, mention_author=False)
    
    @bot.command(name='reload', help='Reload the knowledge base (admin only)')
    @commands.has_permissions(administrator=True)
    async def reload(ctx):
        """Reload the knowledge base from documents"""
        await ctx.send("🔄 Reloading knowledge base... This may take a moment.")
        
        try:
            async with ctx.typing():
                await asyncio.to_thread(bot.rag_engine.reload_knowledge_base)
            
            await ctx.send("✅ Knowledge base reloaded successfully!")
        except Exception as e:
            await ctx.send(f"❌ Error reloading knowledge base: {str(e)}")
    
    @reload.error
    async def reload_error(ctx, error):
        """Handle reload command errors"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need administrator permissions to reload the knowledge base.")
    
    @bot.command(name='info', help='Get information about the bot')
    async def info(ctx):
        """Display bot information"""
        embed = discord.Embed(
            title=f"ℹ️ {Config.BOT_NAME}",
            description="A RAG-powered Discord bot that answers questions using a knowledge base.",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="How to use",
            value=f"Use `{Config.COMMAND_PREFIX}ask <your question>` to ask a question!",
            inline=False
        )
        
        embed.add_field(
            name="Technology",
            value="Powered by LangChain, OpenAI, and ChromaDB",
            inline=False
        )
        
        embed.set_footer(text="Made for university club members")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='ping', help='Check if the bot is responsive')
    async def ping(ctx):
        """Check bot latency"""
        latency = round(bot.latency * 1000)
        await ctx.send(f'🏓 Pong! Latency: {latency}ms')
    
    return bot


def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()
        
        # Set up and run bot
        bot = setup_bot()
        bot.run(Config.DISCORD_BOT_TOKEN)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
    except Exception as e:
        print(f"Error starting bot: {e}")


if __name__ == "__main__":
    main()
