from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import threading
import uuid

API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

bot = Client(
    "streambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app = FastAPI()

FILES = {}


@bot.on_message(filters.video | filters.document)
async def video_handler(client, message):

    unique_id = str(uuid.uuid4())

    FILES[unique_id] = {
        "chat_id": message.chat.id,
        "message_id": message.id
    }

    stream_link = f"https://your-render-url.onrender.com/watch/{unique_id}"
    download_link = f"https://your-render-url.onrender.com/download/{unique_id}"

    await message.reply_text(
        f"▶ Stream:\n{stream_link}\n\n⬇ Download:\n{download_link}"
    )


@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/watch/{file_id}")
async def watch(file_id: str):

    return HTMLResponse(f"""
    <video width="100%" controls autoplay>
        <source src="/download/{file_id}">
    </video>
    """)


@app.get("/download/{file_id}")
async def download(file_id: str):

    file_data = FILES.get(file_id)

    if not file_data:
        return {"error": "file not found"}

    return {
        "message": "Streaming system setup complete"
    }


def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=10000)


threading.Thread(target=run_fastapi).start()

bot.run()
