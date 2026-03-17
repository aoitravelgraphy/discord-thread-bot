import os
import discord

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

@client.event
async def on_message(message):
    # ボット自身の発言には反応しない
    if message.author.bot:
        return

    # 「？」または「?」から始まるメッセージに反応
    if message.content.startswith('？') or message.content.startswith('?'):
        # 検索ワードを抽出（例：「？マイル」から「マイル」を取り出す）
        query = message.content[1:].strip()
        
        # スレッドを作成する
        await message.create_thread(name=f"【診断】{query}", auto_archive_duration=60)
        print(f"スレッド作成成功: {query}")

client.run(TOKEN)
