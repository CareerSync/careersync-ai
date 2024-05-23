import os
from utils.utils import *
import chromadb
import warnings
from prompts.prompts import *

warnings.filterwarnings('ignore')

# 텍스트 파일이 위치한 디렉토리 경로
txt_dir = './'
model = 'gpt-3.5-turbo'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
chroma_client = chromadb.Client()
vectorDB = chroma_client.create_collection(name='BOAZ_data')

def load_data_to_vectorDB(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        for json_document in f:
            embed_doc = get_text_embedding(str(json_document), client)
            store_embedding(embed_doc, str(json_document), vectorDB=vectorDB)
    print("텍스트 벡터DB에 저장 완료")

def process_user_query(input_message):
    query_embeddings = get_text_embedding(input_message, client)
    similar_docs = vectorDB.query(query_embeddings=query_embeddings, n_results=2)
    similar_docs = '\n\n'.join(similar_docs['documents'][0])
    prompted_question = RAGPrompt.simpleQAPrompt.format(context=similar_docs, question=input_message)
    print(f"입력 프롬프트:\n{prompted_question}")
    answer = openai_output(client, model, query=prompted_question)
    print(f"답변:\n{answer}")

if __name__ == '__main__':
    load_data_to_vectorDB("data.jsonl")
    
    while True:
        input_message = input("\n질문을 작성하세요:\n")
        if input_message.lower() == 'quit':
            break
        process_user_query(input_message)