from pyrogram import Client, filters
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn
import threading
import os
import mimetypes

# =========================================
# TELEGRAM API
# =========================================

API_ID = 33604359
API_HASH = "02a8b195fe839d3ed727ca746748db10"
BOT_TOKEN = "7313598031:AAHpI5-UCF3Cyw2QwhiV0gyTUR41oiIvcFY"

# =========================================
# DOMAIN
# =========================================

DOMAIN = "https://telegram-bot-1-az9g.onrender.com"

# =========================================
# PYROGRAM CLIENT
# =========================================

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================================
# FASTAPI
# =========================================

app = FastAPI()

# =========================================
# TEMP DATABASE
# =========================================

FILES = {}

# =========================================
# HOME
# =========================================

@app.get("/")
async def home():

    return {
        "status": "Telegram CDN Streaming Bot Running"
    }

# =========================================
# START COMMAND
# =========================================

@bot.on_message(filters.command("start"))
async def start_command(client, message):

    await message.reply_text(
        "✅ Telegram Streaming Bot Ready\n\n"
        "Send me:\n"
        "• Video\n"
        "• Movie\n"
        "• File\n\n"
        "I will generate:\n"
        "▶ Stream Link\n"
        "⬇ Download Link"
    )

# =========================================
# RECEIVE MEDIA
# =========================================

@bot.on_message(filters.video | filters.document)
async def media_handler(client, message):

    media = message.video or message.document

    if not media:
        return

    file_name = media.file_name or "video.mp4"

    message_id = str(message.id)

    FILES[message_id] = {
        "chat_id": message.chat.id,
        "message_id": message.id,
        "file_name": file_name,
        "file_size": media.file_size
    }

    watch_link = f"{DOMAIN}/watch/{message_id}"
    download_link = f"{DOMAIN}/download/{message_id}"

    await message.reply_text(
        f"✅ File Ready\n\n"
        f"📺 Watch Online:\n"
        f"{watch_link}\n\n"
        f"⬇ Download:\n"
        f"{download_link}"
    )

# =========================================
# WATCH PAGE
# =========================================

@app.get("/watch/{msg_id}", response_class=HTMLResponse)
async def watch_video(msg_id: str):

    html = f"""
    <!DOCTYPE html>

    <html>
    <head>

        <title>Video Player</title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <style>

            body {{
                margin: 0;
                background: black;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            video {{
                width: 100%;
                height: 100%;
                background: black;
            }}

        </style>

    </head>

    <body>

        <video
            controls
            autoplay
            playsinline
            preload="metadata"
        >

            <source
                src="/download/{msg_id}"
                type="video/mp4"
            >

        </video>

    </body>
    </html>
    """

    return HTMLResponse(content=html)

# =========================================
# DOWNLOAD / STREAM
# =========================================

@app.get("/download/{msg_id}")
async def download_video(msg_id: str, request: Request):

    data = FILES.get(msg_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    msg = await bot.get_messages(
        chat_id=data["chat_id"],
        message_ids=data["message_id"]
    )

    media = msg.video or msg.document

    if not media:
        raise HTTPException(
            status_code=404,
            detail="Media unavailable"
        )

    file_size = media.file_size

    mime_type = (
        mimetypes.guess_type(data["file_name"])[0]
        or "application/octet-stream"
    )

    range_header = request.headers.get("range")

    start = 0
    end = file_size - 1

    if range_header:

        bytes_range = range_header.replace(
            "bytes=",
            ""
        )

        start_str, end_str = bytes_range.split("-")

        start = int(start_str)

        if end_str:
            end = int(end_str)

    chunk_size = end - start + 1

    async def file_stream():

        async for chunk in bot.stream_media(
            msg,
            offset=start,
            limit=chunk_size
        ):
            yield chunk

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Disposition": f'inline; filename="{data["file_name"]}"',
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

    return StreamingResponse(
        file_stream(),
        status_code=206 if range_header else 200,
        media_type=mime_type,
        headers=headers
    )

# =========================================
# RUN FASTAPI
# =========================================

def run_fastapi():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

# =========================================
# START SERVICES
# =========================================

threading.Thread(
    target=run_fastapi,
    daemon=True
).start()

print("✅ FastAPI Started")
print("✅ Telegram Bot Started")

bot.run()
