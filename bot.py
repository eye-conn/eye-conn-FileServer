import logging
import requests
import telegram
import json
from telegram import *
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)
# from telegram import (
#   ParseMode
# )

EYECONN_SERVER='http://localhost:8000'
# EYECONN_SERVER='https://eyeconn.herokuapp.com'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def link(update: Update, context: CallbackContext):
    update.message.reply_text(text=f'Enter text shown in accounts page')
    return 1

def getLink(update: Update, context: CallbackContext):
    try: 
      code,username = update.message.text.split()
      chat_id = update.message.chat.id
      # print(code,username,chat_id)
      url = f'{EYECONN_SERVER}/telegram/link/?code={code}&username={username}&chat_id={chat_id}'
      response = requests.get(url)
      d = response.json()
      if d['success']:
        update.message.reply_text(text=f'{d["message"]}')
      else:
        update.message.reply_text(text=f'{d["message"]}')
      return ConversationHandler.END
    except Exception as E:
      print(E)
      update.message.reply_text(text=f'Please follow the format show on website')
      return ConversationHandler.END

def admin(update: Update, context: CallbackContext):
    if update.message.chat.username == 'gauthamd365':
      url = f'{EYECONN_SERVER}/telegram/admin/getUnverifiedAccounts'
      response = requests.get(url)
      d = response.json()
      if d['success'] :
        # update.message.reply_text(text=f'{d["message"]}')
        users = d['users']
        if len(users) == 0:
          update.message.reply_text(text=f'No users to verify')
        
        msg=""
        for user in users:
          msg += f'<b>{user["name"]}</b> - <code>{user["username"]}</code>\n\n'
        update.message.reply_text(text=f'{msg}',parse_mode=ParseMode.HTML)
        return 1
      else:
        print(d['message'])
        update.message.reply_text(text=f'Something went wrong')
        return ConversationHandler.END
    else:
      update.message.reply_text(text=f'Don\'t try to be Oversmart.')
      context.bot.send_message(chat_id=update.message.chat.id, text=f'This phone will enter factory mode in 5 seconds.')
      context.bot.send_message(chat_id='1259041196', text=f'Asshole, {update.message.chat.first_name}\n{update.message.chat.username}')
      return ConversationHandler.END

def enableAccount(update: Update, context: CallbackContext):
    try: 
      usernames = update.message.text.split()
      chat_id = update.message.chat.id
      # print(code,username,chat_id)
      url = f'{EYECONN_SERVER}/telegram/enableAccount'
      response = requests.post(url, json={'usernames':usernames})
      d = response.json()
      if d['success']:
        update.message.reply_text(text=f'{d["message"]}')
      else:
        update.message.reply_text(text=f'{d["message"]}')
      return ConversationHandler.END
    except Exception as E:
      print(E)
      update.message.reply_text(text=f'Please\' follow the format show on website')
      return ConversationHandler.END


def updates(update: Update, context: CallbackContext):
  update.message.reply_text(text=f'{update.message.chat.first_name} your,\nTelegram Username: {update.message.chat.username}\nChat Id: {update.message.chat.id}')
     
def start(update: Update, context: CallbackContext):
  print(update.message.text)
  update.message.reply_text(text=f'Welcome to Eyeconn,\nMr. {update.message.chat.first_name}.\n\nUse /link to link your account with the bot.\n\nFor any queries contact @gauthamd365')



def main()->None:
    updater = Updater("5667527521:AAFBH9JHBU-_I3p2ey4FUehJdGpK85HUXX4",use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('updates', updates))
    dispatcher.add_handler(CommandHandler('user', updates))

    link_handler = ConversationHandler(
        entry_points=[CommandHandler('link', link)],
        states={
            1: [
                MessageHandler(Filters.text, getLink)
            ], 
        },
        fallbacks=[CommandHandler('start', start)],
    )
    dispatcher.add_handler(link_handler)


    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin)],
        states={
            1: [
                MessageHandler(Filters.text, enableAccount)
            ], 
        },
        fallbacks=[CommandHandler('start', start), CommandHandler('link', link)],
    )
    dispatcher.add_handler(admin_handler)

    updater.start_polling()
    updater.idle()

main()
