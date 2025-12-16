from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MAIN_CHANNEL, TARGET_CHANNELS, LOG_CHANNEL
from db import save_forwarded_message, get_forwarded_messages, delete_forwarded_message
import asyncio

# Initialize the client
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=[MAIN_CHANNEL]))
async def forward_handler(event):
    """Forward new messages from main channel to target channels."""
    if not TARGET_CHANNELS:
        return

    for target in TARGET_CHANNELS:
        try:
            forwarded = await client.forward_messages(target, event.message)
            save_forwarded_message(MAIN_CHANNEL, event.message.id, target, forwarded.id)
            # Log
            await client.send_message(LOG_CHANNEL, f"Forwarded message {event.message.id} from {MAIN_CHANNEL} to {target}")
        except Exception as e:
            await client.send_message(LOG_CHANNEL, f"Failed to forward message {event.message.id} to {target}: {str(e)}")

@client.on(events.MessageDeleted(chats=[MAIN_CHANNEL]))
async def delete_handler(event):
    """Delete forwarded messages when original is deleted."""
    for msg_id in event.deleted_ids:
        forwarded = get_forwarded_messages(MAIN_CHANNEL, msg_id)
        for f in forwarded:
            try:
                await client.delete_messages(f['forwarded_channel'], [f['forwarded_message_id']])
                await client.send_message(LOG_CHANNEL, f"Deleted forwarded message {f['forwarded_message_id']} from {f['forwarded_channel']}")
            except Exception as e:
                await client.send_message(LOG_CHANNEL, f"Failed to delete forwarded message {f['forwarded_message_id']} from {f['forwarded_channel']}: {str(e)}")
            delete_forwarded_message(MAIN_CHANNEL, msg_id, f['forwarded_channel'])

if __name__ == '__main__':
    client.run_until_disconnected()