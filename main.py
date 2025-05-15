import requests
import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask

TOKEN = "8046771751:AAHAqpQbNofqUn94DlMbnmpkq_aPASlzXnY"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Telegram corriendo."

async def cotizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    data = {
        "asset": "USDT",
        "fiat": "BOB",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 1,
        "tradeType": "BUY"
    }
    headers = {'Content-Type': 'application/json'}
    try:
        res = requests.post(url, json=data, headers=headers).json()
        price = res['data'][0]['adv']['price']
        await update.message.reply_text(f"💵 Precio P2P (BUY): {price} BOB por 1 USDT")
    except Exception as e:
        await update.message.reply_text("❌ Error al obtener la cotización.")

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("dolar", cotizacion))
    app_bot.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
