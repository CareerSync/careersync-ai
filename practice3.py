import os
from utils.utils import *
import chromadb
import warnings
from prompts.prompts import *
warnings.filterwarnings('ignore')


# 텍스트 파일이 위치한 디렉토리 경로
txt_dir = './'
model = 'gpt-3.5-turbo'
client = OpenAI(api_key=os.environ.get(api_key))

chroma_client = chromadb.Client()
vectorDB = chroma_client.create_collection(name='BOAZ_data')

if __name__ == '__main__':
    with open("data.jsonl", "r", encoding='utf-8') as f:
        for json_document in f:
            embed_doc = get_text_embedding(str(json_document))
            store_embedding(embed_doc, str(json_document), vectorDB=vectorDB)
    print("텍스트 벡터DB에 저장 완료")
    for _ in range(10**6):
        input_message = input("\n질문을 작성학세요:\n")
        query_embeddings = get_text_embedding(input_message)
        similar_docs = vectorDB.query(query_embeddings=query_embeddings, n_results=2)
        similar_docs = '\n\n'.join(similar_docs['documents'][0])
        promptedQuestion = RAGPrompt.simpleQAPrompt.format(context=similar_docs, question=input_message)
        print(f"입력 프롬프트:\n{promptedQuestion}")
        Answer = openai_output(query=promptedQuestion, 
                                        model=model,
                                        client=client)
        print(f"답변:\n{Answer}")