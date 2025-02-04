import os
import logging
import yaml
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from deploy import deploy_repository  # Deployment function

# Logging Setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load Configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
ALLOWED_USERS = config.get("allowed_users", [])  # List of allowed Telegram user IDs

# Initialize bot & dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a GitHub repository URL to deploy!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        update.message.reply_text("❌ You are not authorized to use this bot.")
        return

    repo_url = update.message.text.strip()

    if "github.com" not in repo_url:
        update.message.reply_text("❌ Invalid GitHub repository URL. Please send a valid URL.")
        return

    update.message.reply_text(f"🔄 Deploying `{repo_url}` ... Please wait.")

    success, message = deploy_repository(repo_url)

    if success:
        update.message.reply_text(f"✅ Deployment Successful!\n\n{message}")
    else:
        update.message.reply_text(f"❌ Deployment Failed!\n\nError: {message}")

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
