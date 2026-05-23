from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
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

FILES = {}


@app.get("/")
async def home():
    return {"status": "running"}


@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Send me any video/file."
    )


@bot.on_message(filters.media)
async def media_handler(client, message):

    file_id = None

    if message.video:
        file_id = message.video.file_id

    elif message.document:
        file_id = message.document.file_id

    if not file_id:
        return

    message_id = message.id
    chat_id = message.chat.id

    FILES[str(message_id)] = {
        "chat_id": chat_id,
        "message_id": message_id
    }

    watch_link = f"{DOMAIN}/watch/{message_id}"
    download_link = f"{DOMAIN}/download/{message_id}"

    await message.reply_text(
        f"▶ Stream:\n{watch_link}\n\n"
        f"⬇ Download:\n{download_link}"
    )


@app.get("/watch/{msg_id}", response_class=HTMLResponse)
async def watch(msg_id: str):

    html = f"""
    <html>
    <body style="margin:0;background:black;">
    <video width="100%" controls autoplay>
        <source src="/download/{msg_id}" type="video/mp4">
    </video>
    </body>
    </html>
    """

    return html


@app.get("/download/{msg_id}")
async def download(msg_id: str):

    data = FILES.get(msg_id)

    if not data:
        return {"error": "File not found"}

    msg = await bot.get_messages(
        data["chat_id"],
        data["message_id"]
    )

    async def file_stream():

        async for chunk in bot.stream_media(msg):
            yield chunk

    return StreamingResponse(
        file_stream(),
        media_type="video/mp4"
    )


def run_fastapi():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


threading.Thread(target=run_fastapi, daemon=True).start()

bot.run()
