from webshop.bot.main import bot, test_bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update
# from webshop.api.main import api_bp


app = Flask(__name__)


@app.route('/test2')
def index():
    print(10)
    return 20


# @app.route(config.WEBHOOK_PATH, methods=['POST'])
# def webhook():
#     if request.headers.get('content-type') == 'application/json':
#         json_string = request.get_data().decode('utf-8')
#         update = Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         abort(403)


# app.register_blueprint(api_bp)

if __name__ == '__main__':
    print(test_bot)
    # bot.polling()
    import time
    bot.remove_webhook()
    time.sleep(1)
    # bot.set_webhook(
    #     config.WEBHOOK_URL,
    #     certificate=open('webhook_cert.pem', 'r')
    # )
    print(test_bot)
    app.run(debug=True)

