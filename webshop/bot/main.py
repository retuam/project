from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .config import TOKEN
from ..db.models import Text, Category, Products, User, Cart, Order
from .keyboards import START_KB, CART_KB, SINGLE_KB
from .lookups import *


bot = TeleBot(TOKEN)
test_bot = 100


def keyboard(message, txt):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(message.chat.id, txt, reply_markup=kb)


def get_products(category, call, kb):
    products = category.get_products()
    buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{product_lookup}{separator}{product.id}')
               for product in products]
    if buttons:
        kb.add(*buttons)
        bot.edit_message_text(category.title, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=kb)
    else:
        bot.edit_message_text(category.title + Text.objects.get(slug='empty_cat').body, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard(message, Text.objects.get(slug='greetings').body)
    if not User.objects(uid=message.from_user.id):
        User.objects.create(title=message.from_user.username, uid=message.from_user.id)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['categories'])
def categories(message):
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text=Text.objects.get(slug='category').body, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def categories_click(call):
    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()
    if category.is_parent:
        buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in category.subcategories]

        if buttons:
            buttons.append(InlineKeyboardButton(text=Text.objects.get(slug='back').body,
                                                callback_data=f'{category_lookup}{separator}{category_id}'))
            kb.add(*buttons)
            bot.edit_message_text(category.title, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=kb)
        else:
            get_products(category, call, kb)
    else:
        get_products(category, call, kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['discount_products'])
def discounts(message):
    kb = InlineKeyboardMarkup()
    products = Products.get_discounts_product()
    buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{product_lookup}{separator}{product.id}')
               for product in products]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text=Text.objects.get(slug='discount').body, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == product_lookup)
def product_click(call):
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=Text.objects.get(slug='to_cart').body,
                                callback_data=f'{tocart_lookup}{separator}{product.id}'))

    txt = f'''{product.title} \n price: {product.price} \n discount: {product.discount} \n stock: {product.in_stock} 
    \n {product.description}'''

    bot.send_photo(call.message.chat.id, product.image)
    bot.send_message_text(txt, chat_id=call.message.chat.id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == tocart_lookup)
def to_cart_click(call):
    cart = Cart.objects
    cart.user = User.objects(uid=call.from_user.id).first()
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    cart.price = round(product.price * (100 - product.discount), 2)
    cart.product = product
    cart.save()
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(call.message.chat.id, Text.objects.get(slug='add').body, reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['my_cart'])
def my_cart(message):
    carts = Cart.objects(user=User.objects(uid=message.from_user.id).first()).all()
    cart_products = [cart.product for cart in carts]
    if cart_products:
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=product.title, callback_data=f'{change_lookup}{separator}{product.id}')
                   for product in cart_products]
        kb.add(*buttons)
        bot.send_message(message.chat.id, text=Text.objects.get(slug='from_cart').body, reply_markup=kb)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(*[KeyboardButton(text=text) for text in CART_KB.values()])
        bot.send_message(message.chat.id, Text.objects.get(slug='finish').body, reply_markup=kb)
        _txt = Text.objects.get(slug='total').body + f' {cart.price}'
        bot.send_message(message.chat.id, text=_txt)
    else:
        keyboard(message, Text.objects.get(slug='empty').body)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == CART_KB['checkout'])
def checkout(message):
    carts = Cart.objects.get(user=User.objects(uid=message.from_user.id).all())
    for cart in carts:
        Order.objects.create(user=cart.user, products=cart.product, qty=cart.qty, price=cart.price)
        cart.delete()
    bot.send_message(message.chat.id, text=Text.objects.get(slug='checkout').body)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == CART_KB['erase'])
def erase(message):
    carts = Cart.objects.get(user=User.objects(uid=message.from_user.id).all())
    for cart in carts:
        cart.delete()
    bot.send_message(message.chat.id, text=Text.objects.get(slug='empty').body)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == change_lookup)
def from_cart_change(call):
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    cart = Cart.objects(user=User.objects(uid=call.from_user.id).first(), product=product).first()
    change(call, cart)


def change(call, cart):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=SINGLE_KB['plus'], callback_data=f'{plus_lookup}{separator}{cart.id}'))
    kb.add(InlineKeyboardButton(text=SINGLE_KB['minus'], callback_data=f'{minus_lookup}{separator}{cart.id}'))
    kb.add(InlineKeyboardButton(text=SINGLE_KB['delete'], callback_data=f'{fromcart_lookup}{separator}{cart.id}'))
    bot.send_message(call.message.chat.id, text=Text.objects.get(slug='change').first(), reply_markup=kb)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in CART_KB.values()])


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == plus_lookup)
def plus_cart_click(call):
    cart_id = call.data.split(separator)[1]
    cart = Cart.objects.get(id=cart_id)
    cart.qty += 1
    cart.save()
    change(call, cart)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == plus_lookup)
def minus_cart_click(call):
    cart_id = call.data.split(separator)[1]
    cart = Cart.objects.get(id=cart_id)
    if cart.qty > 1:
        cart.qty -= 1
        cart.save()
        change(call, cart)
    else:
        cart.delete()
        keyboard(call.message, Text.objects.get(slug='product_empty').first())


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == fromcart_lookup)
def from_cart_click(call):
    cart_id = call.data.split(separator)[1]
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    keyboard(call.message, Text.objects.get(slug='product_empty').first())
