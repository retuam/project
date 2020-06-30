from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .config import TOKEN
from ..db.models import Text, Category, Products, User, Cart, Order
from .keyboards import START_KB, CART_KB
from .lookups import *


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    txt = Text.objects.get(title=Text.TITLES['greetings']).body
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(message.chat.id, txt, reply_markup=kb)
    if not User.objects(uid=message.from_user.id):
        User.objects.create(title=message.from_user.username, uid=message.from_user.id)
    user = User.objects(uid=message.from_user.id).first()
    if not Cart.objects(user=user):
        Cart.objects.create(user=user)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['categories'])
def categories(message):
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text=Text.TITLES['category'], reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['discount_products'])
def discounts(message):
    kb = InlineKeyboardMarkup()
    products = Products.get_discounts_product()
    buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{product_lookup}{separator}{product.id}')
               for product in products]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text=Text.TITLES['discount'], reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == CART_KB['checkout'])
def checkout(message):
    cart = Cart.objects.get(user=User.objects(uid=message.from_user.id).first())
    Order.objects.create(user=cart.user, products=cart.products)
    cart.products = []
    cart.save()
    bot.send_message(message.chat.id, text=Text.TITLES['checkout'])


@bot.message_handler(content_types=['text'], func=lambda message: message.text == CART_KB['erase'])
def erase(message):
    cart = Cart.objects.get(user=User.objects(uid=message.from_user.id).first())
    cart.products = []
    cart.save()
    bot.send_message(message.chat.id, text=Text.TITLES['erase'])


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['my_cart'])
def my_cart(message):
    cart = Cart.objects(user=User.objects(uid=message.from_user.id).first()).first()
    cart_products = cart.products
    if cart_products:
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{fromcart_lookup}{separator}{product.id}')
                   for product in cart_products]
        kb.add(*buttons)
        bot.send_message(message.chat.id, text=Text.TITLES['from_cart'], reply_markup=kb)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(*[KeyboardButton(text=text) for text in CART_KB.values()])
        bot.send_message(message.chat.id, Text.TITLES['finish'], reply_markup=kb)
    else:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
        bot.send_message(message.chat.id, Text.TITLES['empty'], reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):
    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()
    if category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in subcategories]
        if buttons:
            kb.add(*buttons)
            bot.edit_message_text(category.title, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=kb)
        else:
            bot.edit_message_text(category.title + Text.TITLES['empty_sub'], chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        products = category.get_products()
        buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{product_lookup}{separator}{product.id}')
                   for product in products]
        if buttons:
            kb.add(*buttons)
            bot.edit_message_text(category.title, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=kb)
        else:
            bot.edit_message_text(category.title + Text.TITLES['empty_cat'], chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == product_lookup)
def product_click(call):
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=Text.TITLES['to_cart'], callback_data=f'{tocart_lookup}{separator}{product.id}'))
    bot.edit_message_text(product.title, chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == tocart_lookup)
def to_cart_click(call):
    cart = Cart.objects(user=User.objects(uid=call.from_user.id).first()).first()
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    cart.add_products(product)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(call.message.chat.id, Text.TITLES['add'], reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == fromcart_lookup)
def from_cart_click(call):
    cart = Cart.objects(user=User.objects(uid=call.from_user.id).first()).first()
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    cart.delete_products(product)
    kb = InlineKeyboardMarkup()
    products = Cart.products()
    buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{fromcart_lookup}{separator}{product.id}')
               for product in products]
    kb.add(*buttons)
    bot.send_message(call.message.chat.id, text=Text.TITLES['from_cart'], reply_markup=kb)


def start_bot():
    bot.polling()
