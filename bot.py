import discord
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        await message.create_thread(
            name=message.content[:10],
            auto_archive_duration=60
        )
    except:
        pass

client.run(TOKEN)
