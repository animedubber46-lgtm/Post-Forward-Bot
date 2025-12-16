from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collection for forwarded messages
forwarded_messages = db.forwarded_messages

def save_forwarded_message(original_channel, original_message_id, forwarded_channel, forwarded_message_id):
    """Save a mapping of original message to forwarded message."""
    forwarded_messages.insert_one({
        'original_channel': original_channel,
        'original_message_id': original_message_id,
        'forwarded_channel': forwarded_channel,
        'forwarded_message_id': forwarded_message_id
    })

def get_forwarded_messages(original_channel, original_message_id):
    """Get all forwarded messages for a given original message."""
    return list(forwarded_messages.find({
        'original_channel': original_channel,
        'original_message_id': original_message_id
    }))

def delete_forwarded_message(original_channel, original_message_id, forwarded_channel):
    """Delete a specific forwarded message entry."""
    forwarded_messages.delete_one({
        'original_channel': original_channel,
        'original_message_id': original_message_id,
        'forwarded_channel': forwarded_channel
    })

def get_all_forwarded_for_channel(original_channel):
    """Get all forwarded messages for a channel (for cleanup if needed)."""
    return list(forwarded_messages.find({'original_channel': original_channel}))