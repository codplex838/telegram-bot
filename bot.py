import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["videoBot"]
collection = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    collection.insert_one({
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name
    })

    await update.message.reply_text(
        "Bot + MongoDB working!"
    )

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot started successfully")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    app.run_polling(
        drop_pending_updates=True,
        close_loop=False
    )
