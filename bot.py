from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from pymongo import MongoClient
import uuid

BOT_TOKEN = "7313598031:AAHpI5-UCF3Cyw2QwhiV0gyTUR41oiIvcFY"

MONGO_URL = "mongodb+srv://srinivasaraomahankali97_db_user:Ryx3jbIoh036Nbkc@bread.roaqkqu.mongodb.net/?appName=BREAD"

client = MongoClient(MONGO_URL)

db = client["telegram_bot"]

collection = db["videos"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a video."
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    unique_id = str(uuid.uuid4())[:8]

    data = {
        "unique_id": unique_id,
        "file_id": video.file_id,
        "file_name": video.file_name,
        "file_size": video.file_size,
        "uploader": update.effective_user.id
    }

    collection.insert_one(data)

    await update.message.reply_text(
        f"✅ Saved Successfully!\n\nID: {unique_id}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.VIDEO, handle_video)
    )

    print("MongoDB Bot Started...")

    app.run_polling()

if __name__ == "__main__":
    main()
