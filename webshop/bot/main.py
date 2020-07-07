from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .config import TOKEN
from ..db.models import Text, Category, Products, User, Cart, Order
from .keyboards import START_KB, CART_KB, SINGLE_KB
from .lookups import *


bot = TeleBot(TOKEN)


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


def change(call, cart):
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=SINGLE_KB['plus'], callback_data=f'{plus_lookup}{separator}{cart.id}'),
        InlineKeyboardButton(text=SINGLE_KB['minus'], callback_data=f'{minus_lookup}{separator}{cart.id}'),
        InlineKeyboardButton(text=SINGLE_KB['delete'], callback_data=f'{fromcart_lookup}{separator}{cart.id}')
    ]
    kb.add(*buttons)
    txt = cart.product.title + f' ({cart.qty})\n' + Text.objects(slug='change').first().body
    bot.edit_message_text(txt, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb)


def cat_main():
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    return kb


@bot.message_handler(commands=['start'])
def start(message):
    keyboard(message, Text.objects.get(slug='greetings').body)
    if not User.objects(uid=message.from_user.id):
        User.objects.create(title=message.from_user.username, uid=message.from_user.id)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['categories'])
def categories(message):
    bot.send_message(message.chat.id, text=Text.objects.get(slug='category').body, reply_markup=cat_main())


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == back_lookup)
def categories_back(call):
    bot.edit_message_text(Text.objects.get(slug='category').body, chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=cat_main())


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
                                                callback_data=f'{back_lookup}{separator}{category_id}'))
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
    kb.add(InlineKeyboardButton(text=Text.objects.get(slug='to_cart').title,
                                callback_data=f'{tocart_lookup}{separator}{product.id}'))

    txt = f'''{product.title} 
     - price: {product.price}
     - discount: {product.discount}
     - stock: {product.in_stock}
     
     {product.description}'''

    bot.send_photo(call.message.chat.id, product.image, caption=txt, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == tocart_lookup)
def to_cart_click(call):
    cart = Cart()
    cart.user = User.objects(uid=call.from_user.id).first()
    product_id = call.data.split(separator)[1]
    product = Products.objects.get(id=product_id)
    cart.price = round(product.price * (100 - product.discount) / 100, 2)
    cart.product = product
    cart.save()
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(call.message.chat.id, Text.objects.get(slug='add').body, reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['my_cart'])
def my_cart(message):
    out_cart(message, edt=False)


@bot.callback_query_handler(func=lambda call: call.data == list(CART_KB.keys())[0])
def checkout(call):
    user = User.objects(uid=call.from_user.id).first()
    for cart in Cart.objects(user=user).all():
        Order.objects.create(user=cart.user, product=cart.product, qty=cart.qty, price=cart.price)
        cart.delete()
    bot.edit_message_text(Text.objects.get(slug='checkout').body, chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == list(CART_KB.keys())[1])
def erase(call):
    user = User.objects(uid=call.from_user.id).first()
    for cart in Cart.objects(user=user).all():
        cart.delete()
    bot.edit_message_text(Text.objects.get(slug='empty').body, chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == change_lookup)
def from_cart_change(call):
    product = Products.objects(id=call.data.split(separator)[1]).first()
    user = User.objects(uid=call.from_user.id).first()
    cart = Cart.objects(user=user, product=product).first()
    change(call, cart)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == plus_lookup)
def plus_cart_click(call):
    cart = Cart.objects(id=call.data.split(separator)[1]).first()
    cart.qty += 1
    cart.save()
    change(call, cart)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == minus_lookup)
def minus_cart_click(call):
    cart = Cart.objects(id=call.data.split(separator)[1]).first()
    if cart.qty > 1:
        cart.qty -= 1
        cart.save()
        change(call, cart)
    else:
        cart.delete()
        out_cart(call.message)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == fromcart_lookup)
def from_cart_click(call):
    cart = Cart.objects(id=call.data.split(separator)[1]).first()
    cart.delete()
    out_cart(call.message)


def out_cart(msg, edt=True):
    user = User.objects(uid=msg.from_user.id).first()
    cart_products = [_ for _ in Cart.objects(user=user).all()]
    if cart_products:
        kb = InlineKeyboardMarkup()
        kb.add(*[InlineKeyboardButton(text=f'{cart.product.title} ({cart.qty})',
                                      callback_data=f'{change_lookup}{separator}{cart.product.id}')
                 for cart in cart_products])
        kb.add(*[InlineKeyboardButton(text=value, callback_data=key) for key, value in CART_KB.items()])
        _from_cart_txt = Text.objects.get(slug='from_cart').body
        _total_txt = Text.objects.get(slug='total').body
        _txt = f'{_from_cart_txt}\n{_total_txt} {Cart.user_price(user)}'
        if edt:
            bot.edit_message_text(_txt, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kb)
        else:
            bot.send_message(msg.chat.id, text=_txt, reply_markup=kb)
    else:
        if edt:
            bot.edit_message_text(Text.objects.get(slug='empty').body, chat_id=msg.chat.id, message_id=msg.message_id)
        else:
            bot.send_message(msg.chat.id, text=Text.objects.get(slug='empty').body)
