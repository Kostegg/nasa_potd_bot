import logging
from operator import contains

from config import tg_api_token
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from api.nasa import apod
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! This bot doesn't contain alot right now.\n"
                                                                          "use /pic to get a picture or /help to get more info!")

async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        info = apod(context.args[0])
        if info.get("code") is not None or len(context.args) != 1:
            await (context.bot.send_message(chat_id=update.effective_chat.id, text="Please input correct date in YYYY-MM-DD format!"))
            return
    else:
        info = apod(None)
    await (context.bot.send_photo(chat_id=update.effective_chat.id, photo=info["url"]))
    await (context.bot.send_message(chat_id=update.effective_chat.id, text=info["explanation"]+"\n"
                                                                           +"Copyright: "
                                                                           +(info["copyright"] if "copyright" in info else "")+"\n"+
                                    "Date of APOD: "+info["date"]))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await (context.bot.send_message(chat_id=update.effective_chat.id, text="Here are the commands that are usable with this bot:\n"
                                                                           "/start - Start the bot and get a small message\n"
                                                                           "/help - Displays this message\n"
                                                                           "/pic [date in YYYY-MM-DD format or nothing] - sends a NASA APOD of specific date or of the current day"))

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await (context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't support any interactions with me beside '/start', '/help' and '/pic' commands at the moment"))


if __name__ == '__main__':
    application = ApplicationBuilder().token(f'{tg_api_token}').build()

    start_handler = CommandHandler('start', start)
    pic_handler = CommandHandler('pic', pic)
    help_handler = CommandHandler('help', help)
    unknown_handler = MessageHandler(None, unknown)
    application.add_handler(start_handler)
    application.add_handler(pic_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()