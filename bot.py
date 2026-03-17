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
    print(f"--- 検索キーワード: {query} ---")

    try:
        response = notion.databases.query(database_id=DATABASE_ID)
        
        for page in response['results']:
            props = page['properties']
            
            # Name列（タイトル）の取得
            name_obj = props.get('Name', {}).get('title', [])
            actual_name = name_obj[0]['plain_text'] if name_obj else ""
            
            if actual_name == query:
                print(f"✅ 「{query}」を発見しました。回答を抽出します。")
                
                # Description列の取得（あらゆる形式に対応）
                desc_prop = props.get('Description', {})
                desc_data = desc_prop.get('rich_text', [])
                
                answer = ""
                if desc_data:
                    # 複数のテキストが入っていても全部連結する
                    answer = "".join([t['plain_text'] for t in desc_data])
                
                if answer:
                    thread = await message.create_thread(name=query, auto_archive_duration=60)
                    await thread.send(answer)
                    print(f"✨ 送信完了!")
                    return
                else:
                    print(f"⚠️ Descriptionが空、または形式が違います。")
                    await message.channel.send(f"「{query}」は見つかりましたが、回答（Description）が空っぽです。")
                    return

        await message.channel.send(f"Notionに「{query}」という項目が見つかりませんでした。")

    except Exception as e:
        print(f"❌ エラー発生: {e}")
