import os
import logging
import yaml
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from deploy import deploy_repository  # Deployment function

# Logging Setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load Configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
ALLOWED_USERS = config.get("allowed_users", [])  # List of allowed Telegram user IDs

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

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()