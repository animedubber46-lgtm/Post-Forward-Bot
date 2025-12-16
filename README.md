# Telegram Channel Forwarding Bot

This bot forwards messages from a main channel to multiple target channels and synchronizes deletions.

## Setup

1. Install dependencies: `pip install -r requirements.txt`

2. Fill in `config.py` with your credentials:
   - API_ID, API_HASH: From https://my.telegram.org/
   - BOT_TOKEN: From @BotFather
   - OWNER_ID: Your Telegram user ID
   - MONGO_URI: MongoDB connection string
   - LOG_CHANNEL: Channel ID for logs
   - MAIN_CHANNEL: Channel ID where content is uploaded
   - TARGET_CHANNELS: List of channel IDs to forward to

3. Ensure the bot is added as admin to MAIN_CHANNEL and all TARGET_CHANNELS.

4. Run the bot: `python main.py`

## How it works

- When a new message is posted in MAIN_CHANNEL, it is forwarded to all TARGET_CHANNELS.
- When a message is deleted in MAIN_CHANNEL, the corresponding forwarded messages are deleted from TARGET_CHANNELS.
- All actions are logged to LOG_CHANNEL.