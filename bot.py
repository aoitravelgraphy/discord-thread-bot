import os
import discord
from notion_client import Client

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

notion = Client(auth=NOTION_TOKEN)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ログイン成功: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot: return
    if not (message.content.startswith('？') or message.content.startswith('?')): return

    query = message.content[1:].strip()
    print(f"--- 検索開始: {query} ---")

    try:
        # データベースから全件取得
        response = notion.databases.query(database_id=DATABASE_ID)
        
        for page in response['results']:
            props = page['properties']
            
            # 1. 「Name」列（タイトル）から文字を抽出
            name_data = props.get('Name', {}).get('title', [])
            actual_name = name_data[0]['plain_text'] if name_data else ""
            
            print(f"チェック中: {actual_name}")

            # 2. 文字が一致したら回答を探す
            if actual_name == query:
                desc_data = props.get('Description', {}).get('rich_text', [])
                if desc_data:
                    answer = desc_data[0]['plain_text']
                    # スレッドを作成して回答を送信
                    thread = await message.create_thread(name=query, auto_archive_duration=60)
                    await thread.send(answer)
                    print(f"送信完了: {actual_name}")
                    return # 見つかったら終了

        # 最後まで見つからなかった場合
        await message.channel.send(f"「{query}」という項目がNotionで見つかりませんでした。")

    except Exception as e:
        print(f"エラー発生: {e}")
        await message.channel.send("エラーが起きました。設定を確認してください。")

client.run(TOKEN)
