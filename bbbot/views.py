import time
import json
import os
import hashlib
from django.views.generic.base import View
import requests
from django.http import HttpResponse
from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater

from django import views
from django.views.generic import CreateView
from .models import BotUser, User,Message
from .forms import RegisterForm
from django.conf import settings
from django.utils import timezone
from django.shortcuts import  render

 


def hello(views):
    return HttpResponse('<h2>Just Home</h2>')
 
class VVVV(CreateView):
    def v(update: Update, context: CallbackContext,request):
        user = update.message.from_user.id
        x = BotUser.objects.get(user_id=user)
         
        return render(request,'bb/user_profile.html',{"userr":user})

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    
    # Start the Bot
    # updater.start_polling()
    """ updater.start_webhook(listen="0.0.0.0",
                          port=int(settings.PORT),
                          url_path=settings.TOKEN,
                          webhook_url='https://dj-botq.herokuapp.com/' + settings.TOKEN) """
    updater.idle()


if __name__ == '__main__':
    main()
