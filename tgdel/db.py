from .models import BotUser
from telegram import Update
from telegram.ext import CallbackContext


def save_botuser(update: Update, context: CallbackContext):
    fromm = update.message.from_user
    BotUser.objects.get_or_create(
        chat_id = fromm['id'],
        username=fromm['username'],
        last_name=fromm['last_name'],
        first_name=fromm['first_name'],
    )