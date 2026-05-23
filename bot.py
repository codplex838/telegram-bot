from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7313598031:AAHpI5-UCF3Cyw2QwhiV0gyTUR41oiIvcFY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me any video and I will return its Telegram file_id."
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    file_id = video.file_id

    await update.message.reply_text(
        f"FILE ID:\n\n{file_id}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.VIDEO, handle_video)
    )

    print("Bot started successfully...")

    app.run_polling()

if __name__ == "__main__":
    main()
