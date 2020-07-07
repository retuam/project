from webshop.bot.main import bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update
from webshop.api.main import api_bp
import time


app = Flask(__name__)


@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(
    config.WEBHOOK_URL,
    certificate=open('webhook_cert.pem', 'r')
)
app.register_blueprint(api_bp)
# app.run(debug=True)


if __name__ == '__main__':
    pass
    # bot.polling()
