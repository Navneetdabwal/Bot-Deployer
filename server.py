from flask import Flask, request
import telegram
import os
import threading
import logging
from bot import bot, dispatcher  # Import bot instance & dispatcher

# Logging Setup
logging.basicConfig(level=logging.INFO)

# Flask app setup
app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Get bot token from environment variable
PORT = int(os.environ.get("PORT", 5000))  # Default port 5000, but Render provides a dynamic port
WEBHOOK_URL = f"https://your-app.onrender.com/{TOKEN}"  # Replace with your Render app URL

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    """Receive update from Telegram and process it."""
    update = telegram.Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!", 200

def set_webhook():
    """Set Telegram Webhook"""
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to: {WEBHOOK_URL}")

if __name__ == "__main__":
    # Set webhook in a separate thread
    threading.Thread(target=set_webhook).start()
    app.run(host="0.0.0.0", port=PORT)
