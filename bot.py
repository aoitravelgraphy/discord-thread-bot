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
    print(f"ログインしました: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('？') or message.content.startswith('?'):
        query = message.content[1:].strip() 

        try:
            response = notion.databases.query(
                database_id=DATABASE_ID,
                filter={
                    "property": "Name",
                    "rich_text": {
                        "contains": query
                    }
                }
            )

            if response['results']:
                result = response['results'][0]
                answer = result['properties']['Description']['rich_text'][0]['plain_text']
                
                thread = await message.create_thread(
                    name=query, 
                    auto_archive_duration=60
                )
                await thread.send(answer)
            else:
                await message.channel.send(f"「{query}」に関する回答が見つかりませんでした。")

        except Exception as e:
            print(f"エラー: {e}")

client.run(TOKEN)
