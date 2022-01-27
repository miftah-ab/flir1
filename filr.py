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

os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()

from bbbot.models import BotUser, Likes
from bbbot.helper import set_user, MessageCreationView, set_profile, set_bot_user
from cities_light.models import City

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, AGE, LOCATION, PHONE = range(4)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Boy', 'Girl']]

    update.message.reply_text(
        'Please select Gender?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['gender'] = text
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)

    update.message.reply_text(
        'How old are you?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return AGE


def proper_age(update: Update, context: CallbackContext):
    update.message.reply_text(
        'What is your real age ?'
    )


def age(update: Update, context: CallbackContext) -> int:
    # while update.message.text >= str(18):
    #    gender(update, context)  # this may repeat job

    while True:
        try:
            # text.isdigit() and (18 < int(text) < 100):
            text = int(update.message.text)
            if 17 < text < 100:
                context.user_data['age'] = text
                user = update.message.from_user

                logger.info("Age of %s: %s", user.first_name, update.message.text)
                update.message.reply_text(
                    'Enter your city',
                )

            elif 18 > text > 0:

                print('Not designed for child')
                update.message.reply_text('Not designed for child')
                ##############33
            else:
                update.message.reply_text('What is your real age ? \nMust be over 18')
        except (AssertionError, ValueError):
            update.message.reply_text('What is your real age ? \nMust be over 18')
            # return update.message.text
        if text < 0:
            print("Sorry, your response must not be negative.")
            update.message.reply_text('Negative AGE !')
            continue
        else:
            break
    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    context.user_data['location'] = text
    user = update.message.from_user
    logger.info("City of %s: %s", user.first_name, update.message.text)
    location_keyb = KeyboardButton(text='Share Contact', request_contact=True)
    loc_keyb = [[location_keyb]]
    reply = ReplyKeyboardMarkup(loc_keyb, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Please share your Phone Number \n'
                              'No one see your Phone Number with out your permission ', reply_markup=reply)

    return PHONE


def phone(update: Update, context: CallbackContext) -> int:
    # text = update.message.text.lower()
    # context.user_data['choice'] = text
    user = update.message.from_user
    logger.info("Phone of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(context.user_data)
    set_bot_user(update, context)  # /************
    update.message.reply_text(
        'Congratulation !! FINISHED \n'
        'ALL MUST SAVED IN ADMIN',
        reply_markup=ReplyKeyboardRemove(),
    )
    menu(update, context)
    return ConversationHandler.END


def show_data(update: Update, context: CallbackContext) -> None:
    """Display the gathered info."""
    update.message.reply_text(
        f"This is what you already told me: {facts_to_str(context.user_data)}"
    )


def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('canceled', reply_markup=ReplyKeyboardRemove(), )
    return ConversationHandler.END


def user_format(stories_user):
    # fo = f'{BotUser.first_name}\n {BotUser.age} \t\t\t\t {BotUser.location} '
    if BotUser.gender == 'boy':
        for stories_user in BotUser.objects.filter(gender='boy'):
            # vv = BotUser.objects.filter()
            print(stories_user)
            print(stories_user.gender)
            return f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                   f'\n {stories_user.age} \t\t\t\t {stories_user.location} '

        else:
            for stories_user in BotUser.objects.filter(gender='girl'):
                # vv = BotUser.objects.filter()
                print(stories_user)
                print(stories_user.gender)
                return f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                       f'\n {stories_user.age} \t\t\t\t {stories_user.location} '


def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [['🔞 Stories', '\U00002747 Start ✳️'],
                ['💘 Matches', '💓 Likes You'],
                ['Settings', '💸', '💌']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Home Page 👇', reply_markup=reply_markup)


def stories(update: Update, context: CallbackContext) -> None:
    x = update.message.from_user.id
    y = context.user_data
    z = BotUser.objects.get(user_id=x)
    print(z.user_id)
    print(z.gender)
    print(z.first_name)
    """for cc in BotUser.objects.filter(user_id=x):
        print(z.user_id)
        print(z.gender)
        print(z.first_name) """
    if z.gender == 'boy':  # y['gender'] this is not filter by db it's by pickle file
        for stories_user in BotUser.objects.filter(gender='boy'):
            # vv = BotUser.objects.filter()
            print(stories_user)
            print(stories_user.gender)
            update.message.reply_text(f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                                      f'\n {stories_user.age} \t\t\t\t {stories_user.location} \t\t\t\t'
                                      f'{stories_user.gender}')
    elif z.gender == 'girl':
        for stories_user in BotUser.objects.filter(gender='girl'):
            # vv = BotUser.objects.filter()
            print(stories_user)
            print(stories_user.gender)
            update.message.reply_text(f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                                      f'\n {stories_user.age} \t\t\t\t {stories_user.location}\t\t\t\t'
                                      f'{stories_user.gender}')

    else:
        update.message.reply_text('Something wrong please try again or contact support')


def start_filter_menu(update: Update, context: CallbackContext, ) -> None:
    keyboard = [['❌', '💚'],
                ['⬅️ Back', '🎁'], ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('This Start is under construction 👇', reply_markup=reply_markup)
    x = update.message.from_user.id
    z = BotUser.objects.all()
    # print random user
    # print(z.ramdom)
    # update.message.reply_text('x', random.z)
    start_filter(update, context)


def start_filter(update: Update, context: CallbackContext, ) -> None:
    # if update.message.text == '\U00002747 Start ✳️':
    print('get ....')
    # if update.message.text == '💚':  # comment out this is unnecessary
    x = update.message.from_user.id
    y = context.user_data
    z = BotUser.objects.get(user_id=x)
    print(z.user_id)
    print(z.gender)
    print(z.first_name)
    if z.gender == 'boy':  # y['gender'] this is not filter by db it's by pickle file
        for stories_user in BotUser.objects.filter(gender='girl'):
            # like mideregew sew
            global too
            to1 = stories_user.user_id
            print(f'hhhh    {to1}')
            too = BotUser.objects.get(user_id=to1)
            print(f'kkkkkkk   {too}')
            print(stories_user)
            print(stories_user.gender)
            update.message.reply_text(f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                                      f'\n {stories_user.age} \t\t\t\t {stories_user.location} \t\t\t\t'
                                      f'{stories_user.gender}')
            # waiting for like or dislike then user2
            if update.message.text == '💚':
                print('liked')
                # try catch to prevent duplication
                Likes.objects.get_or_create(
                    user_from=z,
                    user_to=too,
                )
                update.message.reply_text('Liked Saved!!! ')

        update.message.reply_text('No suitable user')
    elif z.gender == 'girl':
        for stories_user in BotUser.objects.filter(gender='boy'):
            print(random.Random.choice(stories_user))
            # vv = BotUser.objects.filter()
            # global too
            to1 = stories_user.user_id
            print(f'hhhh    {to1}')
            too = BotUser.objects.get(user_id=to1)
            print(f'kkkkkkk   {too}')
            print(stories_user)
            print(stories_user.gender)
            update.message.reply_text(f'{stories_user.first_name}\t\t\t\t\t {stories_user.user_id} ' \
                                      f'\n {stories_user.age} \t\t\t\t {stories_user.location}\t\t\t\t'
                                      f'{stories_user.gender}')
            if update.message.text == '💚':
                print('liked')

                update.message.reply_text('Liked ')
                break
    else:
        update.message.reply_text('Something wrong please try again or contact support')
    """ if update.message.text == '💚':
         update.message.reply_text('like saving .....')
         Likes.objects.create(
            user_from=z,
            user_to=too,
         )
         update.message.reply_text('finished ')
         print('liked')
         update.message.reply_text('Liked ') """

    if update.message.text == '⬅️ Back':
        print('back')
        menu(update, context)
    else:
        update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def matches(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ['⬅️ Back', ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('This Matches is under construction 👇', reply_markup=reply_markup)
    cuser = update.message.from_user.id
    x = BotUser.objects.get(user_id=cuser)
    print(x.first_name)
    fromm = Likes.objects.filter(user_from=x)
    print(fromm)
    # print(fromm.user_to)
    # print(fromm.user_from.user_id)
    for m in Likes.objects.filter(user_to=x):
        print(m.user_from.first_name)
        for vv in Likes.objects.filter(user_from=x):
            print(vv.user_to.first_name)
            print(vv.user_to.user_id)
            if vv.user_to.user_id == m.user_from.user_id:
                update.message.reply_text(f'Matches \n {m.user_from.first_name}, {m.user_from.user_id}')

        # for m in Likes.objects.filter(user_from=l):  if
        # if  user from current
        # if m user like cuser ???

    if update.message.text == '⬅️ Back':
        print('back')
        menu(update, context)
    else:
        update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def likes_you_keybord(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This Likes You page is under construction')
    keyboard = [['⏪', '⏩ '],
                ['⬅️ Back'], ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('This Start is under construction 👇', reply_markup=reply_markup)
    likes_you(update, context)


def likes_you(update: Update, context: CallbackContext) -> None:
    if update.message.text == '⏩ ':
        like = Likes.objects.all()
        if like:  # not used
            user = update.message.from_user.id
            x = BotUser.objects.get(user_id=user)
            print(x.first_name)

            for l in Likes.objects.filter(user_to=x):
                print(l)
                print(l.user_from.first_name)
                update.message.reply_text(f'this user like you \n {l.user_from.first_name}, {l.user_from.user_id}')
                # fromm = Likes.objects.filter(user_from=l.user_from)
                # print(fromm.user_from)
                if update.message.text == '⏩ ':
                    pass
                else:
                    print('⏩ jj')
                    update.message.reply_text('⏩ jj')
                return
        else:
            print('No likes yet vv')
            update.message.reply_text('No likes yet vv')

        if update.message.text == '⬅️ Back':
            print('back')
            menu(update, context)
        else:
            update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def setting(update: Update, context: CallbackContext) -> None:
    setting_keyboard = [['👤 My profile', '🔍 Search settings'],
                        ['⬅️ Back']]
    reply_markup = ReplyKeyboardMarkup(setting_keyboard, resize_keyboard=True)
    update.message.reply_text('Settings ', reply_markup=reply_markup)

    if update.message.text == '👤 My profile':
        print('jj')
        keyboard = [['⬅️ Back']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text('vv ', reply_markup=reply_markup)
        idd = update.message.from_user.id
        user = BotUser.objects.get(user_id=idd)  # try with id==number
        update.message.reply_text(f'{user.first_name}, {user.age} ' \
                                  f'\n   {user.location}\t\t\t\t'
                                  f'\n Gender: {user.gender} \t\t\t\t\t\t\t\t\t\t\t\t{user.user_id}')
        if update.message.text == '⬅️ Back':
            setting(update, context)

    elif update.message.text == '🔍 Search settings':
        update.message.reply_text('Wait for moment please')
    elif update.message.text == '⬅️ Back':
        print('back')
        menu(update, context)

        # update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def profile(update: Update, context: CallbackContext) -> None:
    # print current user profile
    keyboard = [['⬅️ Back']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('vv ', reply_markup=reply_markup)
    idd = update.message.from_user.id
    user = BotUser.objects.get(user_id=idd)  # try with id==number
    update.message.reply_text(f'{user.first_name}, {user.age} ' \
                              f'\n   {user.location}\t\t\t\t'
                              f'\n Gender: {user.gender} \t\t\t\t\t\t\t\t\t\t\t\t{user.user_id}')
    if update.message.text == '⬅️ Back':
        print('back')
        setting(update, context)  # menu
    else:
        update.message.reply_text('Wrong Input ❗ press 👇👇👇')


def cancel_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('menu removed', reply_markup=ReplyKeyboardRemove(), )


def home_select(update: Update, context: CallbackContext):
    if update.message.text == '🔞 Stories':
        stories(update, context)
    elif update.message.text == '\U00002747 Start ✳️':
        start_filter_menu(update, context)
    elif update.message.text == '💘 Matches':
        matches(update, context)
    elif update.message.text == '💓 Likes You':
        likes_you_keybord(update, context)
    elif update.message.text == 'Settings':
        setting(update, context)
    elif update.message.text.startswith('/'):
        update.message.reply_text('command detected..')
        menu(update, context)
    elif update.message.text == '💌':
        update.message.reply_text('Love letter retriving....')
    elif update.message.text == 'vv':
        update.message.reply_text('haha seems ....')
    else:
        menu(update, context)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='con')
    updater = Updater("1900859603:AAE3wfQth3zd2G0g7pGoKcD8Anxwfdth5Gk", persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl)$'), gender)],
            AGE: [MessageHandler(Filters.regex('^(1[89]|[2-9][0-9])$') & ~Filters.command, age)],
            # filter (^(0-9) only number   r'\d+',^([2-9]\d|[1-9])$
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, location)],
            PHONE: [MessageHandler(Filters.contact, phone)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # it may useful for onetime
        name='my_conv',
        persistent=True,

    )
    dispatcher.add_handler(conv_handler)
    show_data_handler = CommandHandler('show_data', show_data)
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CommandHandler('cmenu', cancel_menu))
    dispatcher.add_handler(show_data_handler)
    # dispatcher.add_handler(CommandHandler('h', home_select))
    # dispatcher.add_handler(MessageHandler(Filters.all, home_select))
    setting_keyboardd = ['👤 My profile', '🔍 Search settings', 'vv']
    home_sel = ['🔞 Stories', '\U00002747 Start ✳️',
                '💘 Matches', '💓 Likes You',
                'Settings', '💸', '💌']
    start_f = ['❌', '💚',
               '⬅️ Back', '🎁']
    likes_y = ['⏪', '⏩ ',
               '⬅️ Back'],

    """set_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Settings)$'), setting)],
        states=[

        ],
        fallbacks=[],
    )
    """
    dispatcher.add_handler(MessageHandler(Filters.text(setting_keyboardd), setting))
    dispatcher.add_handler(MessageHandler(Filters.text(home_sel), home_select))
    dispatcher.add_handler(MessageHandler(Filters.text(start_f), start_filter))
    dispatcher.add_handler(MessageHandler(Filters.text(likes_y), likes_you))
    # dispatcher.add_handler(MessageHandler(Filters.regex('^(\U00002747 Start ✳️|Settings)$'), home_select))
    # dispatcher.add_handler(MessageHandler(Filters.all, setting))

    """
    dispatcher.add_handler(MessageHandler(Filters.all, stories))
    dispatcher.add_handler(MessageHandler(Filters.all, matches))
    dispatcher.add_handler(MessageHandler(Filters.all, start_filter))
    dispatcher.add_handler(MessageHandler(Filters.all, likes_you))
    dispatcher.add_handler(MessageHandler(Filters.all, setting))
    dispatcher.add_handler(MessageHandler(Filters.all, profile))"""

    """ dispatcher.add_handler(MessageHandler(Filters.regex(r'🔞 Stories'), stories))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(💘 Matches|⬅️ Back)$'), matches))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(\U00002747 Start ✳️|⬅️ Back|💚)$'), start_filter))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(💓 Likes You|⬅️ Back)$'), likes_you))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Settings|⬅️ Back)$'), setting))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(👤 My profile|⬅️ Back)$'), profile))
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
