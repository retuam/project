from webshop.bot.main import bot, test_bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update
from webshop.api import main as amn


app = Flask(__name__)
# app.register_blueprint(amn.api_bp)


# @app.route('/', methods=['GET'])
# def index():
#     print(1)
#     return 2
#
#
# @app.route('/test', methods=['GET'])
# def test():
#     print(10)
#     return 20


@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


if __name__ == '__main__':
    print(test_bot)
    # bot.polling()
    import time
    bot.remove_webhook()
    print(test_bot)
    time.sleep(1)
    bot.set_webhook(
        config.WEBHOOK_URL,
        certificate=open('webhook_cert.pem', 'r')
    )
    # app.run(debug=True)
