from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import threading
import os

API_ID = 33604359
API_HASH = "02a8b195fe839d3ed727ca746748db10"
BOT_TOKEN = "7313598031:AAHpI5-UCF3Cyw2QwhiV0gyTUR41oiIvcFY"

DOMAIN = "https://telegram-bot-1-az9g.onrender.com"

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "Bot Running Successfully"}


@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Send me any video or file and I will generate stream/download links."
    )


@bot.on_message(filters.video | filters.document)
async def generate_link(client, message):

    file_id = message.video.file_id if message.video else message.document.file_id

    stream_link = f"{DOMAIN}/watch/{file_id}"
    download_link = f"{DOMAIN}/download/{file_id}"

    await message.reply_text(
        f"▶ Stream Link:\n{stream_link}\n\n⬇ Download Link:\n{download_link}"
    )


from fastapi.responses import RedirectResponse


@app.get("/watch/{file_id}")
async def watch_video(file_id: str):

    file = await bot.get_messages("me", ids=1)

    tg_file = await bot.download_media(file_id)

    return RedirectResponse(url=tg_file)


@app.get("/download/{file_id}")
async def download_video(file_id: str):

    tg_file = await bot.download_media(file_id)

    return RedirectResponse(url=tg_file)


def run_fastapi():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)


threading.Thread(target=run_fastapi).start()

bot.run()
