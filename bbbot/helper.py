import json
from urllib import request

import requests
from django.http import HttpResponse
from django.views.generic import CreateView
from requests.sessions import session
from telegram import Update
from telegram.ext import CallbackContext, BasePersistence

from .models import User, Message, Profile, BotUser

j_data = {'Name': 'Abaa', 'age': 44, 'city': 'Addis', 'hasChildren': False, 'title': ['Programmer', 'ENGINEER']}
j_data1 = {'title': 'hahu', 'body': 'This is from dic'}
data = json.dumps(j_data, indent=4)


# may be not working bc of argument in django
# ""                    "" didn't get url in PTB
# last try in tgbot.py by calling/copy for using commands ....1
# worked by simply call this method in standalone app(tgbot.py)


def set_user(update: Update, context: CallbackContext) -> None:
    fromm = update.message.from_user
    # phone0 = update.message.contact
    phone1 = update.message.contact.phone_number
    # lat = update.message.location.latitude
    # lon = update.message.location
    User.objects.create(
        # auther=chat_idd,
        Tuser_id=fromm['id'],
        username=fromm['username'],
        first_name=fromm['first_name'],
        last_name=fromm['last_name'],
        is_bot=fromm['is_bot'],
        language_code=fromm['language_code'],
        phone=phone1,
        # lat=lat,
        # lon=lon['longitude'],
        # phone=phone0['phone_number']
        # h=fromm.username,
        # t=text,
    )


def set_bot_user(update: Update, context: CallbackContext) -> None:
    fromm = update.message.from_user
    phone1 = update.message.contact.phone_number
    x = context.user_data
    BotUser.objects.create(

        user_id=fromm['id'],
        username=fromm['username'],
        first_name=fromm['first_name'],
        last_name=fromm['last_name'],

        phone=phone1,  # work ??  see if it print in conversation
        age=x['age'],
        gender=x['gender'],
        location=x['location']

    )


def set_profile(update: Update, context: CallbackContext) -> None:
    #  dataa = update.message.text
    x = context.user_data
    userr = update.message.from_user.id
    # if id exist  else create id
    # user = User.Tuser_id

    try:
        user = User.objects.get(Tuser_id=userr)
        Profile.objects.create(
            buser=user,
            age=x['agee'],
            gender=x['gender'],
            location=x['location']
        )
        update.message.reply_text('Saved See in Admin !!')
    except Exception as e:
        # not only for value it work for all
        if ValueError:
            update.message.reply_text(e)


class MessageCreationView(CreateView):
    model = Message

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def set_message(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat
        text = update.message.text
        message_id = update.message.message_id
        Message.objects.create(
            text=text,
            message_id=message_id,
            chat_id=chat_id['id'],

        )
