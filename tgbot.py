import logging
import pickle
from uuid import uuid4
from typing import Dict
import telegram
from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    PicklePersistence
# from  ptbcontrib.postgres_persistence import  P
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()

from bbbot.models import User
from bbbot.helper import  set_user, MessageCreationView,  set_profile
from cities_light.models import City

print('req')


"""

q = input('enter name   ')
city = City.objects.filter(name__istartswith=q)
for c in city:
    print(c)

coun = city.count()
print(coun)
ch = 1
for y in city:
    for x in range(ch, coun+1):
        print(x, y)
        ch = ch + 1
        break
    # print(f'{x},{c}')

cho = input('insert your city  ')
print(y)
"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Age', 'Favourite colour'],
    ['Number of siblings', 'Something else...'],
    ['Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def sav(update: Update, context: CallbackContext) -> str:
    # facts_to_str(context.user_data)
    update.message.reply_text(context.user_data)
    x = context.user_data
    # idd = x['id']
    # print(idd)
    print(x['agee'])
    set_profile(update, context)




def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    reply_text = "Hi! My name is Doctor Botter."
    if context.user_data:
        reply_text += (
            f" You already told me your {', '.join(context.user_data.keys())}. Why don't you "
            f"tell me something more about yourself? Or change anything I already know."
        )
    else:
        reply_text += (
            " I will hold a more complex conversation with you. Why don't you tell me "
            "something about yourself?"
        )
    update.message.reply_text(reply_text, reply_markup=markup)

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text.lower()
    context.user_data['choice'] = text
    if context.user_data.get(text):
        reply_text = (
            f'Your {text}? I already know the following about that: {context.user_data[text]}'
        )
    else:
        reply_text = f'Your {text}? Yes, I would love to hear about that!'
    update.message.reply_text(reply_text)

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    text = update.message.text
    category = context.user_data['choice']
    context.user_data[category] = text.lower()
    del context.user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(context.user_data)}"
        "You can tell me more, or change your opinion on something.",
        reply_markup=markup,
    )

    return CHOOSING


def show_data(update: Update, context: CallbackContext) -> None:
    """Display the gathered info."""
    update.message.reply_text(
        f"This is what you already told me: {facts_to_str(context.user_data)}"
    )


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(context.user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def unpickle(update: Update, context: CallbackContext):
    infile = open('conversationbot', 'rb')
    new_dict = pickle.load(infile)
    infile.close()

    print(new_dict)
    update.message.reply_text(context.user_data.keys())  # Try WITH value()
    update.message.reply_text(context.chat_data)
    update.message.reply_text(context.bot_data)
    for key, value in new_dict.items():
        print(key, value)
        # print(value)
        # update.message.reply_text(context.user_data.value)


GENDER, PHOTO, LOCATION, BIO = range(4)


def conv(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Boy', 'Girl']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# Define a few command handlers. These usually take the two arguments update and
# context.
def startt(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('Usual')
    context.bot.send_message(chat_id=update.effective_chat.id, text='FROM DJ Standalone')


def sett_post(update: Update, context: CallbackContext) -> None:
    # set_post(update, context)
    update.message.reply_text('See in Admin, \n Not --> correct set_post method in helper \n But the '
                              'This WOrk')


def sett_user(update: Update, context: CallbackContext) -> None:
    set_user(update, context)
    update.message.reply_text('See in Admin, User Saved!!!')


def sett_message(update: Update, context: CallbackContext) -> None:
    set_message = MessageCreationView()
    set_message.set_message(update, context)
    # set_message(update, context)
    update.message.reply_text('See in Admin, Message Saved!!!')


def print_message(update: Update, context: CallbackContext) -> None:
    x = update.message.text
    print(x)
    update.message.reply_text(x)


def location_kbd(update: Update, context: CallbackContext) -> None:
    location_keyb = KeyboardButton(text='Share Location', request_location=True)
    loc_keyb = [[location_keyb]]
    replyx = ReplyKeyboardMarkup(loc_keyb, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Please share your location \n'
                              'No one see your actual location', reply_markup=replyx)


def contact_kbd(update: Update, context: CallbackContext):
    location_keyb = KeyboardButton(text='Share Contact', request_contact=True)
    loc_keyb = [[location_keyb]]
    replyx = telegram.ReplyKeyboardMarkup(loc_keyb, resize_keyboard=True)
    update.message.reply_text('Please share your contact \n'
                              'No one see your contact', reply_markup=replyx)
    # update.message.reply_text('your phone :' + '+2514488')
    # , update.message.contact.phone_number
    # first print
    # set_user(update, context)


def sett_contact(update: Update, context: CallbackContext) -> None:
    set_user(update, context)
    update.message.reply_text('See in Admin, Phone Number and User Saved!!!')


# one function for request one for handler
# store phone no in one model
# try with manual contact insert

def sett_location(update: Update, context: CallbackContext) -> None:
    set_user(update, context)
    update.message.reply_text('See in Admin, Phone Number Saved!!!')


def age(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('age ?')
    agee = update.message.text
    print(agee)
    update.message.reply_text(f'Your age  {agee} ')


def pp(update: Update, context: CallbackContext) -> None:
    x = update.message.from_user.first_name
    print(x)
    update.message.reply_text(f'Name  :{x}')
    # age(update, context)
    contact_kbd(update, context)  # *******************
    # location_kbd(update, context)
    # if not work type manually in side kbd
    # sett_user(update, context)
    p = update.message.contact.phone_number
    print(p)
    update.message.reply_text(f'phone :{p}')
    # set_phone(update, context)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    name = update.message.text
    update.message.reply_text('thanks from echo')


def savvv(update: Update, context: CallbackContext) -> None:
    set_user(update, context)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    update = Update
    context = CallbackContext
    persistence = PicklePersistence(filename='bot1')
    updater = Updater("1900859603:AAE3wfQth3zd2G0g7pGoKcD8Anxwfdth5Gk", persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("startt", startt))
    dispatcher.add_handler(CommandHandler("setuser", sett_user))
    dispatcher.add_handler(CommandHandler("setc", sett_contact, Filters.contact))
    dispatcher.add_handler(CommandHandler("pp", pp))
    # dispatcher.add_handler(MessageHandler(Filters.location, sett_location))
    dispatcher.add_handler(MessageHandler(Filters.contact, sett_contact))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, sett_message))

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Age|Favourite colour|Number of siblings)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="my_conversation",
        persistent=True,
    )
    dispatcher.add_handler(CommandHandler("unpic", unpickle))
    dispatcher.add_handler(CommandHandler('tdj', sav))
    dispatcher.add_handler(conv_handler)

    show_data_handler = CommandHandler('show_data', show_data)
    dispatcher.add_handler(show_data_handler)

    """
    my_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            TITLE: [
                CommandHandler('cancel', cancel),
                # has to be before MessageHandler to catch `/cancel` as command, not as `title`
                MessageHandler(Filters.text, get_title)
            ],
            TEXT: [
                CommandHandler('cancel', cancel),
                # has to be before MessageHandler to catch `/cancel` as command, not as `text`
                MessageHandler(Filters.text, get_text)
            ],
            COMMENTS: [
                CommandHandler('cancel', cancel),
                # has to be before MessageHandler to catch `/cancel` as command, not as `comments`
                MessageHandler(Filters.text, get_comments)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(my_conversation_handler)

    """
    """
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('conv', conv)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl)$'), gender)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location)
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    """

    # Start the Bot
    updater.start_polling()
    print('Running... [Press Ctrl+C to stop]')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    print('Stoping...')


if __name__ == '__main__':
    main()
