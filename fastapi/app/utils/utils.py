# -*- coding: utf-8 -*- 
# 위에거 주석 아니에요. 빼지 마세요 (for 한글)

import json
import warnings
warnings.filterwarnings('ignore')
import os
import time
from openai import OpenAI
import uuid
from datetime import datetime
 
api_key = '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' # 환경 변수 읽기

if api_key is None:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
os.environ["OPENAI_API_KEY"] = api_key

API_MAX_RETRY = 16
API_RETRY_SLEEP = 10
API_ERROR_OUTPUT = "$ERROR$"

def get_text_embedding(document:str, client): # Transform
    embedding = client.embeddings.create(input=document,
                                 model='text-embedding-ada-002').data[0].embedding
    return embedding

def store_embedding(embed_document, document, vectorDB): # Load
    vectorDB.add(
        ids=str(uuid.uuid4()),
        documents=document,
        embeddings=embed_document
    )


def openai_output(client, model, openai_input):
    model = model
    input_message=[{"role": "user", "content": openai_input}]
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=input_message,
                n=1,
                temperature=0,
            )
            output = response.choices[0].message.content
            break
        except Exception as e:
            print(f"ERROR DURING OPENAI API: {e}") 
            time.sleep(API_RETRY_SLEEP)
    return output