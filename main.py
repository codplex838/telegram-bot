from pyrogram import Client, filters
from fastapi import FastAPI
import uvicorn
import threading
import os

API_ID = 33604359
API_HASH = "02a8b195fe839d3ed727ca746748db10"
BOT_TOKEN = "7313598031:AAHpI5-UCF3Cyw2QwhiV0gyTUR41oiIvcFY"

BOT_USERNAME = "telegram-bot-1-az9g.onrender.com"

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "Bot Running"}


@bot.on_message(filters.video | filters.document)
async def generate_link(client, message):

    file_id = message.video.file_id if message.video else message.document.file_id

    stream_link = f"https://{BOT_USERNAME}/watch/{file_id}"
    download_link = f"https://{BOT_USERNAME}/download/{file_id}"

    await message.reply_text(
        f"▶ Stream:\n{stream_link}\n\n⬇ Download:\n{download_link}"
    )


def run_fastapi():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)


threading.Thread(target=run_fastapi).start()

bot.run()
