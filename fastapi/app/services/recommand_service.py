import requests
from services.db_service import *
from services.gpt_service import *
from services.redis_service import *


async def intent_classifier(question):
    url = "http://213.173.108.11:18320/classify"
    body={"user_query":question}
    class_data=requests.get(url, json=body)
    return class_data


async def get_data(user_id,question):
    class_data= intent_classifier(question)

    if class_data==1:
        chroma=chromadb_func()
        question_embbeding=chroma.get_text_embedding(question)
        datas=chroma.query_embedding(question_embbeding,10)
        filtered_data=[{"title":data['title']\
                        ,"siteUrl":data['url']\
                        ,"imgUrl":data['logo']\
                        ,"endDate":data['end_date']\
                        ,"education":data['Education']\
                        ,"workHistory":data['Work_history']\
                        ,"companyName":data['Co_name']} for data in datas]
        return filtered_data
    
    elif class_data==2:
        gpt_func= gpt_func()
        redis_func=redis_func()
        data=gpt_func.interest_extraction(question)
        if data =="No":
            return
        else:
            tech_list = [tech.strip() for tech in data.split(',')]
        user_tech=redis_func.get_tech(user_id)
        for i in tech_list:
            if i not in user_tech:
                user_tech.append(i)
        redis_func.set_tech(user_id, user_tech)
        return

    else:
        return 
    