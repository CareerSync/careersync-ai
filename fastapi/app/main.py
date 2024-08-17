from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from services.gpt_service import *
from services.redis_service import *
from services.recommand_service import *
import os
import asyncio

   
app=FastAPI()

class Item_answer(BaseModel):
    answer: str
class Item_input(BaseModel):
    chat_uuid: str
    user_id: str
    question: str

@app.get("/chatbot/", summary="Root 테스트 API")
def read_root():
    return {"Hello": "World"}

@app.get("/chatbot/chat", summary="질문 요청 APi", response_model=Item_answer,
        responses={
        200: {
            "content": {
            "application/json": {
                "example": "오늘 강남구 개포동 아침 날씨는 맑고 기온은 29.4℃입니다. 강수확률은 0.0%이며, 남실바람이 불고 습도는 47.0%입니다."
            }
        }}})

async def chat(Item: Item_input):
    """
    # 입력 파라미터
    ## chat_uuid : 채팅방 고유 ID
    ## question : 유저의 질문
    # 반환 값
    ## answer : 봇의 답변
    """
    gpt = gpt_func()
    get_data=await get_data(Item.user_id,Item.question)
    answer=gpt.Rag_output(Item.user_id, Item.chat_uuid, Item.question)
    if get_data:
        json={
            "is_true":True,
            "jobPosts":get_data,
            "answer":answer
        }
    return json.dumps(json)



    