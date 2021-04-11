import os
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT'))
APP_URL = os.environ.get('APP_URL')

logger.info('TOKEN="%s"', TOKEN)
logger.info('PORT="%s"', PORT)
logger.info('APP_URL="%s"', APP_URL)

def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url=APP_URL + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
