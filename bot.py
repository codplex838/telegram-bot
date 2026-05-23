import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Connection
client = MongoClient(MONGO_URI)

# Database Name
db = client["videoBot"]

# Collection Name
collection = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Save user data to MongoDB
    collection.insert_one({
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name
    })

    await update.message.reply_text(
        "Hello! Webhook bot + MongoDB working successfully!"
    )

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Webhook bot started...")

    app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 10000)),
    url_path=BOT_TOKEN,
    webhook_url=f"{RENDER_URL}/{BOT_TOKEN}",
    drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
