import os
import discord

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN が読み込めません。Railway の環境変数を確認してください。")

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
        print("スレッド作成成功")
    except Exception as e:
        print(f"スレッド作成失敗: {e}")

client.run(TOKEN)

