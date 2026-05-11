import json
from datetime import datetime

from database_nosql import get_redis

class ChatService:
    def __init__(self):
        self.redis = get_redis()

    def save_message(self, username, text):
        message_data = {
            "username": username,
            "text": text
        }
        self.redis.rpush("chat_history", json.dumps(message_data))
        self.redis.ltrim("chat_history", -50, -1)

    def get_history(self):
        if not self.redis:
            return []
        history = self.redis.lrange("chat_history", 0, -1)
        return [json.loads(m) for m in history]