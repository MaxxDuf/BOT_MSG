import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime

# =========================
# LOAD TOKEN
# =========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# CONFIG
# =========================
ARCANE_BOT_ID = 1217870452253397082
TARGET_CHANNEL_ID = 1499033370632654862

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# LOG FUNCTION
# =========================
def log(msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] {msg}")

# =========================
# READY
# =========================
@bot.event
async def on_ready():
    log(f"CONNECTÉ EN TANT QUE {bot.user}")

# =========================
# MESSAGE HANDLER
# =========================
@bot.event
async def on_message(message):

    # ignore bots sauf Arcane
    if message.author.bot and message.author.id != ARCANE_BOT_ID:
        return

    # debug
    log("=== MESSAGE DETECTE ===")
    log(f"Auteur: {message.author}")
    log(f"Content: {repr(message.content)}")
    log(f"Embeds: {len(message.embeds)}")
    log(f"Attachments: {len(message.attachments)}")

    # filtre Arcane
    if message.author.id == ARCANE_BOT_ID:

        content = message.content

        # fallback si message vide
        if not content and message.embeds:
            embed = message.embeds[0]
            content = embed.title or embed.description or "Message Arcane (embed)"

        if not content:
            content = "Message Arcane sans texte lisible"

        # build message
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)

        if target_channel:
            try:
                # envoyer texte
                await target_channel.send(content)

                # envoyer images si existantes
                for att in message.attachments:
                    await target_channel.send(att.url)

                log("MESSAGE TRANSFERE OK")

            except Exception as e:
                log(f"ERREUR ENVOI: {e}")

        # delete original
        try:
            await message.delete()
            log("MESSAGE SUPPRIME")
        except Exception as e:
            log(f"ERREUR DELETE: {e}")

    await bot.process_commands(message)

# =========================
# RUN
# =========================
bot.run(TOKEN)
