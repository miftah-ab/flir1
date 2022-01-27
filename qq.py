import logging
import pickle
from uuid import uuid4
from typing import Dict
import telegram
from django.http import HttpResponse
from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    PicklePersistence
# from  ptbcontrib.postgres_persistence import  P
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()

from django.views.generic import CreateView
from bbbot.models import BotUser

from django.shortcuts import render

print('kiko')


def hello(views):
    return HttpResponse('<h2>Just Home</h2>')


class VVV(CreateView):
    message = None
    request = None

    def fun1(self, update: Update, context: CallbackContext):
        user = update.message.from_user.id
        x = BotUser.objects.get(user_id=user)
        print(x.first_name)
        update.message.reply_text(f'this user is {x.first_name}')
        # return render(request,'bb/user_profile.html',{"userr":user})

    def fun2(self, update: Update, context: CallbackContext):
        x = self.request.user
        print(x.user_id)
        print(x.last_login)

    def fun3(self, update: Update, context: CallbackContext, request):
        x = self.request.user
        print(x.first_name, x.user_id)


def st(update: Update, context: CallbackContext):
    update.message.reply_text('start_polling......')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1900859603:AAE3wfQth3zd2G0g7pGoKcD8Anxwfdth5Gk00")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    x = VVV()
    # x.fun1(CommandHandler('vv1', x.fun1))
    dispatcher.add_handler(CommandHandler('f1', x.fun1))
    dispatcher.add_handler(CommandHandler('f2', x.fun2))
    dispatcher.add_handler(CommandHandler('f3', x.fun3))
    dispatcher.add_handler(CommandHandler('st', st))
    # on different commands - answer in Telegram

    # Start the Bot
    updater.start_polling()
    """ updater.start_webhook(listen="0.0.0.0",
                          port=int(settings.PORT),
                          url_path=settings.TOKEN,
                          webhook_url='https://dj-botq.herokuapp.com/' + settings.TOKEN) """
    updater.idle()


if __name__ == '__main__':
    main()
