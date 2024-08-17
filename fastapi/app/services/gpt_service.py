from openai import OpenAI
from dotenv import load_dotenv
from services.prompt import interest_prompt
from services.db_service import *
import os
model='gpt-4o'

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

# .env 파일 로드
load_dotenv(dotenv_path)

print(os.getenv('GPT_KEY'))
class gpt_func:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('GPT_KEY'))  
        self.chromadb_func=chromadb_func()

    def Rag_output(self,username, chat_uuid, question):
        prompted_question=self.chromadb_func.prompt_enginnering(username, chat_uuid ,question)
        input_message=[{"role": "user", "content": prompted_question}]
        print(input_message)
        response = self.client.chat.completions.create(
            model=model,
            messages=input_message,
            n=1,
            temperature=0,
        )
        output = response.choices[0].message.content
        return output
    
    def interest_extraction(self,question):
        prompted_question=interest_prompt.format(Input=question)
        input_message=[{"role": "user", "content": prompted_question}]
        response = self.client.chat.completions.create(
            model=model,
            messages=input_message,
            n=1,
            temperature=0,
        )
        output = response.choices[0].message.content
        return output