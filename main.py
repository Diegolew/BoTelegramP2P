import requests
import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Telegram corriendo."

# Función del bot
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

# Lógica del bot en un hilo separado
def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("dolar", cotizacion))
    application.run_polling()

if __name__ == '__main__':
    # Iniciar bot en hilo paralelo
    threading.Thread(target=run_bot).start()
    
    # Iniciar servidor Flask para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
