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
    if message.author.bot:
        return

    if message.content.startswith('？') or message.content.startswith('?'):
        query = message.content[1:].strip()
        print(f"--- 診断開始: 検索ワード「{query}」 ---")

        try:
            # 全件取得して、中身がどう見えているかログに出す
            db_data = notion.databases.query(database_id=DATABASE_ID)
            
            found = False
            for page in db_data['results']:
                # Notion上の「Name」という名前の列を探す
                props = page['properties']
                name_prop = props.get('Name', {})
                
                # タイトルの中身を取り出す
                actual_name = ""
                if 'title' in name_prop and name_prop['title']:
                    actual_name = name_prop['title'][0]['plain_text']
                
                print(f"Notionにあるデータを確認中: 「{actual_name}」")

                if actual_name == query:
                    print("一致するデータを見つけました！回答を準備します。")
                    desc_prop = props.get('Description', {})
                    if 'rich_text' in desc_prop and desc_prop['rich_text']:
                        answer = desc_prop['rich_text'][0]['plain_text']
                        thread = await message.create_thread(name=query, auto_archive_duration=60)
                        await thread.send(answer)
                        found = True
                        break
            
            if not found:
                print(f"エラー: Notionの中に「{query}」と完全に一致するNameが見つかりませんでした。")
                await message.channel.send(f"「{query}」と一致する項目がNotionにありません。")

        except Exception as e:
            print(f"致命的なエラーが発生しました: {e}")
            await message.channel.send("エラーが起きました。ログを確認してください。")

client.run(TOKEN)
