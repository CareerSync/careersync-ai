import os
from utils.utils import *
import chromadb
import warnings
from prompts.prompts import *


client = OpenAI(api_key='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')
chroma_client = chromadb.HttpClient(host='172.22.0.4', port=8000)
vectorDB = chroma_client.create_collection(name='test-law')

def load_data_to_vectorDB(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        for json_document in f:
            embed_doc = get_text_embedding(str(json_document), client)
            store_embedding(embed_doc, str(json_document), vectorDB=vectorDB)
    print("텍스트 벡터DB에 저장 완료")


if __name__ == '__main__':
    load_data_to_vectorDB("subset.jsonl")