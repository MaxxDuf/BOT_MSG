import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# charge le .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# IDs
ID_BOT_ARCANE = 1217870452253397082
CHANNEL_NOTIFICATION_ID = 1499033370632654862

# intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):

    # ignore autres bots
    if message.author.id != ID_BOT_ARCANE:
        return

    content = message.content or ""

    # filtre level up
    if "has reached level" in content:

        channel = bot.get_channel(CHANNEL_NOTIFICATION_ID)

        if channel:
            await channel.send(content)

        try:
            await message.delete()
        except:
            print("Impossible de supprimer le message")

    await bot.process_commands(message)

bot.run(TOKEN)
