from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import threading
import os
import uuid

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

VIDEOS_DIR = "videos"

os.makedirs(VIDEOS_DIR, exist_ok=True)


@app.get("/")
async def home():
    return {"status": "running"}


@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Send me video/file and I will generate stream links."
    )


@bot.on_message(filters.video | filters.document)
async def generate_links(client, message):

    unique_id = str(uuid.uuid4())

    file_path = await message.download(
        file_name=f"{VIDEOS_DIR}/{unique_id}.mp4"
    )

    watch_link = f"{DOMAIN}/watch/{unique_id}"
    download_link = f"{DOMAIN}/download/{unique_id}"

    await message.reply_text(
        f"✅ File Uploaded\n\n"
        f"▶ Stream:\n{watch_link}\n\n"
        f"⬇ Download:\n{download_link}"
    )


@app.get("/watch/{video_id}", response_class=HTMLResponse)
async def watch(video_id: str):

    video_file = f"{VIDEOS_DIR}/{video_id}.mp4"

    html_content = f"""
    <html>
    <body style="margin:0;background:black;">
    <video width="100%" height="100%" controls autoplay>
        <source src="/download/{video_id}" type="video/mp4">
    </video>
    </body>
    </html>
    """

    return html_content


@app.get("/download/{video_id}")
async def download(video_id: str):

    video_file = f"{VIDEOS_DIR}/{video_id}.mp4"

    return FileResponse(
        path=video_file,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )


def run_fastapi():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


threading.Thread(target=run_fastapi).start()

bot.run()
