"""
Command handlers
https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.commandhandler.html?highlight=CommandHandler
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from .db import save_botuser
# Write your command handlers here


# Example: /start
def start(update, context):
    save_botuser(update, context)
    update.message.reply_text(
        text='Hello!'
    )

def simple_text(update, context):
    update.message.reply_text('Simple Text in commands --> 2nd 1st=start')

# Example: /cancel
def cancel(update, context):

    update.message.reply_text(
        text='The action is cancelled in ...'
    )

    return ConversationHandler.END
