from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from .models import BotUser, Product


def my_product_keyboard(update: Update, context: CallbackContext):
    product_keyboard = [['Canceled', 'Pending'],
                         ['Approved', '?'],]
    update.message.reply_text('Select Category',
                              reply_markup=ReplyKeyboardMarkup(product_keyboard,
                                                               one_time_keyboard=True,
                                                               resize_keyboard=True,
                                                               ))


def my_product(update: Update, context: CallbackContext):
    cuser = update.message.from_user.id
     
    user = BotUser.objects.get(user_id=cuser)
    
    
    if update.message.text == 'Pending' :
        for product in Product.objects.filter(user=user, pending=True): # and canceld
            update.message.reply_text(f'Title  {product.title}\n Price  {product.price}\n'
            f'Description  {product.description}\n\n  #{product.categoty}')
    
    elif update.message.text == 'Opened':
        for product in Product.objects.filter(user=user, approved=True): 
            update.message.reply_text(f'Title  {product.title}\n Price  {product.price}\n'
            f'Description  {product.description}\n\n  #{product.categoty}')
        else:
            update.message.reply_text('No approved product')
    elif update.message.text == 'Declined':
        for product in Product.objects.filter(user=user, approved=False): 
            update.message.reply_text(f'Title  {product.title}\n Price  {product.price}\n'
            f'Description  {product.description}\n\n  #{product.categoty}')        
                                                                       
    else:
        update.message.reply_text('Something wrong please try again or contact support')
 

def setting(update: Update, context: CallbackContext):
    setting_keyboard = [['^', 'Wait~'],
                                ]
    update.message.reply_text('press 👇👇👇',
                              reply_markup=ReplyKeyboardMarkup(setting_keyboard,
                                                               one_time_keyboard=True,
                                                               resize_keyboard=True,
                                                               ))
