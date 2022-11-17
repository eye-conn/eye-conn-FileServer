import logging
import telegram
from telegram import *
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def updates(update: Update, context: CallbackContext):
  update.message.reply_text(text=f'{update.message.chat.first_name} your,\nTelegram Username: {update.message.chat.username}\nChat Id: {update.message.chat.id}')
     
def start(update: Update, context: CallbackContext):
  print(update.message.chat.id)
  update.message.reply_text(text=f'Welcome to Eyeconn,\nMr. {update.message.chat.first_name}.\n\nGreetings from \nGagan & Karthik')



def main()->None:
    updater = Updater("5667527521:AAFBH9JHBU-_I3p2ey4FUehJdGpK85HUXX4",use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('updates', updates))
    dispatcher.add_handler(CommandHandler('user', updates))

    updater.start_polling()
    updater.idle()

main()
