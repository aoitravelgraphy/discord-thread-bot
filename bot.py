import discord
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"起動完了: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.Thread):
        return

    # メッセージの先頭10文字をそのままタイトルにしてスレッド作成
    await message.create_thread(
        name=message.content[:10],
        auto_archive_duration=60
    )

client.run(TOKEN)
