import discord
import os

# 変数名を統一し、どちらの環境変数名でも動くようにします
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    raise ValueError("トークンが読み込めません。RailwayのVariablesを確認してください。")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"起動完了: {client.user}")

@client.event
async def on_message(message):
    # ボットの発言には反応しない
    if message.author.bot:
        return

    # 「？」から始まる時だけスレッドを作る
    if message.content.startswith('？') or message.content.startswith('?'):
        try:
            # メッセージの最初の10文字をスレッド名にする
            thread_name = message.content[:10]
            await message.create_thread(
                name=thread_name,
                auto_archive_duration=60
            )
            print(f"スレッド作成成功: {thread_name}")
        except Exception as e:
            print(f"スレッド作成失敗: {e}")

client.run(TOKEN)
