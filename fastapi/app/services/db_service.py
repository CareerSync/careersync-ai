import chromadb
from services.redis_service import *
from dotenv import load_dotenv
import os
from openai import OpenAI
from services.prompt import simpleQAPrompt
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

# .env 파일 로드
load_dotenv(dotenv_path)
client = OpenAI(api_key=os.getenv('GPT_KEY'))

model="gpt-4o"

class chromadb_func:
    def __init__(self):
        chroma_client = chromadb.HttpClient(host='20.41.115.19', port=8000)
        self.vectorDB = chroma_client.get_collection(name='test')
        self.redis_func=redis_func()

    def query_embedding(self,embed_document, n_results):
        similar_docs=self.vectorDB.query(query_embeddings=embed_document, n_results=n_results)
        return similar_docs['documents'][0]

    def get_text_embedding(self, document): # Transform
        embedding = client.embeddings.create(input=document,
                                    model='text-embedding-ada-002').data[0].embedding
        return embedding
    
    def prompt_enginnering(self, username, chat_uuid ,question, language):
        question_embedding=self.get_text_embedding(question,5)
        prev_conversation = self.redis_func.get_conversations(username, chat_uuid)
        similar_docs = self.query_embedding(question_embedding)
        similar_docs = '\n\n'.join(similar_docs)
        prompted_question = simpleQAPrompt.format(context=similar_docs, prev_conversation= prev_conversation , question=question,language=language)
        return prompted_question

