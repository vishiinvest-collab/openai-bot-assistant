from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Привет! Я @AlmaTrBot")

def translate(update, context):
    update.message.reply_text("🔄 Перевод: (тут будет результат)")

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tr", translate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
