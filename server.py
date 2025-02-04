from flask import Flask
import threading
from bot import main  # Import Telegram bot function

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    main()  # Start the Telegram bot

if __name__ == '__main__':
    # Run Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run Flask web server
    app.run(host='0.0.0.0', port=5000)