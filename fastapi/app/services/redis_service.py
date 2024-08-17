
from redis import Redis
import json

class redis_func:
    def __init__(self):
        self.redis_client = Redis(host='career.redis.cache.windows.net', port=6379,db=0,password='7Kcs5X5sPsmrAhEv3fb5HUpJDE1sB5g4rAzCaF6E37Q=')

    def get_conversations(self, user_id, chat_uuid):
        key = f"{user_id}:{chat_uuid}"
        conversations = self.redis_client.lrange(key, 0, -1)
        return [json.loads(conv) for conv in conversations]

    def get_tech(self, user_id):
        key = f"{user_id}"
        tech = self.redis_client.lindex(key, 0)
        return json.loads(tech) 

    def set_tech(self, user_id, tech):
        key = f"{user_id}"
        json={
            user_id: tech
        }
        self.redis_client.set(key, json.dumps(json))
        return "success"