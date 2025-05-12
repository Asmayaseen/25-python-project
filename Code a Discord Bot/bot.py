import os
import discord # type: ignore
from discord.ext import commands # type: ignore
from dotenv import load_dotenv # type: ignore

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Required for message access
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello from Asma's Bot! 👋")

# Run bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: Token not found in .env file.")
