import json
from redis import Redis
import pyodbc

server = 'careersync.database.windows.net'
database = 'local'
username = 'careersync-admin'
password = 'mro8GVNUpl!'
driver= '{ODBC Driver 17 for SQL Server}'


redis_client = Redis(host='172.22.0.5', port=6379,db=0)

def add_conversation(user_id, chatroom_id, user_message, bot_response):
    key = f"user:{user_id}:chatroom:{chatroom_id}:conversations"
    
    # 대화 쌍 생성
    conversation = {
        "user_message": user_message,
        "bot_response": bot_response
    }

    # 대화 추가 (JSON 형식으로 저장)
    redis_client.rpush(key, json.dumps(conversation))
    
    # 대화 길이가 5를 초과하면 오래된 대화 삭제
    if redis_client.llen(key) > 5:
        redis_client.lpop(key)

def init_conversation(user_id, chatroom_id):
    key = f"user:{user_id}:chatroom:{chatroom_id}:conversations"
    redis_client.delete(key)

def load_conversation(user_id, chatroom_id):
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT TOP 5 name, collation_name FROM sys.databases")
            row = cursor.fetchone()
            while row:
                print (str(row[0]) + " " + str(row[1]))
                row = cursor.fetchone()


def get_conversations(user_id, chatroom_id):
    key = f"user:{user_id}:chatroom:{chatroom_id}:conversations"
    conversations = redis_client.lrange(key, 0, -1)
    return [json.loads(conv) for conv in conversations]