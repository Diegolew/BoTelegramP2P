import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

TOKEN = os.getenv("BOT_TOKEN")

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

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("dolar", cotizacion))
    app.run_polling()
