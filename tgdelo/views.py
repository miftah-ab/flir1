import logging
import pickle
import random
from uuid import uuid4
from typing import Dict
import telegram
from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    PicklePersistence
# from  ptbcontrib.postgres_persistence import  P
import os
import django

from .callbacks import my_product, my_product_keyboard, setting

""" os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()
 """

from .db import save_botuser, save_product
from . import constants

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CATEGORY, TITLE, PRICE, DESCRIPTION, PHOTO = range(5)


def start(update: Update, context: CallbackContext):
    save_botuser(update, context)
    setting_keyboard = [['setting', 'My product'],
                        ['Post product', ]]
    reply_markup = ReplyKeyboardMarkup(setting_keyboard, resize_keyboard=True)
    update.message.reply_text(constants.home, reply_markup=reply_markup)


def post_product(update: Update, context: CallbackContext):
    category_keyboard = [['Vehicle', 'Home'],
                         'Electronics', 'Fashion',
                         ['Other']]
    update.message.reply_text('Select Category', reply_markup=ReplyKeyboardMarkup(category_keyboard,
                                                                                  one_time_keyboard=True,
                                                                                  resize_keyboard=True,
                                                                                  input_field_placeholder='Category'))
    return CATEGORY


def category(update: Update, context: CallbackContext):
    category = update.message.text
    context.user_data['category'] = category
    user = update.message.from_user
    logger.info("Category of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Enter Title ',
        reply_markup=ReplyKeyboardRemove(),
    )
    return TITLE


def title(update: Update, context: CallbackContext):
    title = update.message.text
    context.user_data['title'] = title
    user = update.message.from_user
    logger.info("Title of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Enter Price in Birr ')
    return PRICE


def price(update: Update, context: CallbackContext):
    price = update.message.text
    context.user_data['price'] = price
    user = update.message.from_user
    logger.info("Price of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('description')
    return DESCRIPTION


def description(update: Update, context: CallbackContext):
    description = update.message.text
    context.user_data['description'] = description
    user = update.message.from_user
    logger.info("Description of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Photo')
    return PHOTO


def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, update.message.text)
    save_product(update, context)
    update.message.reply_text('Successfully Submitted Wait for Approval \n see in MY product')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('canceled', reply_markup=ReplyKeyboardRemove(), )
    return ConversationHandler.END


def home(update: Update, context: CallbackContext):
    if update.message.text == 'Post product':
        post_product(update, context)
    elif update.message.text == 'My product':
        my_product_keyboard(update, context)
    elif update.message.text == 'setting':
        setting(update, context)
    else:
        update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def main() -> None:
    print('in main')
    persistence = PicklePersistence(filename='del')
    updater = Updater("1900859603:AAE3wfQth3zd2G0g7pGoKcD8Anxwfdth5Gk", persistence=persistence)
    dispatcher = updater.dispatcher
    category_select = ['Vehicle', 'Home',
                       'Electronics', 'Fashion',
                       'Other']
    my_product_select = ['Closed', 'Pending', 'Opened', 'Declined']

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Post product)$'), post_product)],
        states={
            CATEGORY: [MessageHandler(Filters.text(category_select), category)],
            TITLE: [MessageHandler(Filters.text & ~Filters.command, title)],
            PRICE: [MessageHandler(Filters.text & ~Filters.command, price)],
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, description)],
            PHOTO: [MessageHandler(Filters.photo, photo)]
        },
        fallbacks=[CommandHandler('cbu', cancel)],  # it may useful for onetime
        name='del',
        persistent=True, )
    home_select = ['setting', 'My product', 'Post product']
    dispatcher.add_handler(MessageHandler(Filters.text(home_select), home))
    dispatcher.add_handler(MessageHandler(Filters.text(my_product_select), my_product))
    dispatcher.add_handler(CommandHandler('start', start))
    # Start the Bot   
    updater.start_polling()
    print('Running... [Press Ctrl+C to stop]')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    print('Stoping...')
