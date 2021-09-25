import json
import os

import requests
from django.http import HttpResponse
from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater

from django import views
from django.views.generic import CreateView
from .models import User
from .forms import RegisterForm
from django.conf import settings


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    # try with bot.setting send message


def hello(views, ):
    return HttpResponse('juij')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('just simple text in django')


def one():
    bot = Bot(settings.TOKEN)
    bot.send_message('in django token from setting')


def save_user_data(update: Update, context: CallbackContext):
    model = User
    user = update.message.from_user
    usernam = user.username
    print(usernam)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rej", RegisterView))
    dispatcher.add_handler(CommandHandler("one", one))
    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(settings.PORT),
                          url_path=settings.TOKEN,
                          webhook_url='https://portfoli1o1bot.herokuapp.com/' + settings.TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
