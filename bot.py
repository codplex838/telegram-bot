import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Connection
client = MongoClient(MONGO_URI)

# Database
db = client["videoBot"]

# Collection
collection = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Save user in MongoDB
    collection.insert_one({
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name
    })

    await update.message.reply_text(
        "Hello! Bot + MongoDB working successfully!"
    )

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
