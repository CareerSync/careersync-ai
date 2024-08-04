from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.app.utils.func import *
import chromadb
from utils.utils import *
from prompts.prompts import *
from pymongo import MongoClient
model = 'gpt-4o'

client = OpenAI(api_key='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')
chroma_client = chromadb.HttpClient(host='172.22.0.4', port=8000)
vectorDB = chroma_client.get_collection(name='test-law')
mongo= MongoClient("172.22.0.3",27017)
mongodb=mongo['local']
mongodb_collection=mongodb['test']
app=FastAPI()

class Item_chat(BaseModel):
    id: str
    chat_uuid: str
    question: str

class Item_basic(BaseModel):
    id: str
    chat_uuid: str

@app.get("/")
def read_root():
    return {"Hello": "World"}   

@app.post("/chat")
def chatbot(item: Item):
    query_embeddings = get_text_embedding(item.question, client)
    similar_docs = vectorDB.query(query_embeddings=query_embeddings, n_results=2)
    similar_docs = '\n\n'.join(similar_docs['documents'][0])
    prev_conversation = get_conversations(item.id, item.chat_uuid)
    prompted_question = RAGPrompt.simpleQAPrompt.format(context=similar_docs, prev_conversation= prev_conversation , question=item.question)
    answer = openai_output(client, model, openai_input=prompted_question)
    add_conversation(redis_client, item.id, item.chat_uuid, item.question, answer)
    print(prev_conversation)
    mongodb_collection.update_one(
        {"id":item.id,"chat_uuid":item.chat_uuid},
        {"$push": {"question":item.question,"answer":answer}},
        upsert=True 
    )
    return answer

@app.post('/chat/load')
def chat_load(item: Item_basic):
    conversation = get_conversations(item.id, item.chat_uuid)
    return conversation


@app.post("/chat/recommand")
def chat_recommand(item: Item):
    
    print(a)


@app.post("/chat/exit")
def chat_exit(item: Item_basic):
    init_conversation(item.id, item.chat_uuid)
    return {"message": "conversation cleared"}

    