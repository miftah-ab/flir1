from telegram import Update
from telegram.ext import CallbackContext

from .models import BotUser, Product


def save_botuser(update: Update, context: CallbackContext):
    fromm = update.message.from_user
    phone = update.message.contact.phone_number
    BotUser.objects.get_or_create(
        user_id=fromm['id'],
        username=fromm['username'],
        first_name=fromm['first_name'],
        last_name=fromm['last_name'],
        phone=phone,
    )


def save_product(update: Update, context: CallbackContext):
    usert = update.message.from_user.id
    con = context.user_data
    try:
        user = BotUser.objects.get(user_id=usert)
        Product.objects.create(
            user=user,
            category=con['category'],
            title=con['title'],
            price=con['price'],

        )
    except Exception as e:
        pass
