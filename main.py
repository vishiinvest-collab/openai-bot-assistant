from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import asyncio
import logging
import httpx
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8038595183:AAFFtj0X9npHd8srn2h32rMWdjAP8oPsvAI")
bot = Bot(token=BOT_TOKEN)
app = FastAPI()
loop = asyncio.get_event_loop()
dispatcher = Dispatcher(bot, None, workers=1, loop=loop)

# Функция перевода (через OpenAI, DeepL, Google и др. можно позже подключить)
async def translate_text(text: str) -> str:
    # Простой "эмулятор" перевода (можно заменить на API)
    return (
        f"🇷🇺 [RU] Перевод: {text}\n"
        f"🇬🇧 [EN] Translation: {text}\n"
        f"🇨🇳 [CN] 翻译: {text}"
    )

# Обработчик команды /tr
async def tr_command(update: Update, context):
    message = update.message or update.effective_message
    if message.reply_to_message:
        original_text = message.reply_to_message.text
    else:
        original_text = " ".join(context.args)

    if not original_text:
        await message.reply_text("Ответьте на сообщение или введите текст после /tr.")
        return

    translated = await translate_text(original_text)
    await message.reply_text(translated)

# Обработчик корневого запроса
@app.get("/")
async def root():
    return {"message": "Bot is running!"}

# Webhook обработчик
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await dispatcher.process_update(update)
    return {"status": "ok"}

# Подключаем команду
dispatcher.add_handler(CommandHandler("tr", tr_command))
