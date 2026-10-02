# %%
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel


engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

df = pd.read_sql(
    "SELECT * FROM raw_news",
    engine
)
title = df.loc[0, "title"]
content = df.loc[0, "content"]
print(title)
print(content)

prompt = f"""
請分析以下財經新聞。
要求：
1. industry：判斷新聞涉及的產業，可有多個。
2. companies：列出新聞涉及的公司，只包含企業，不包含政府、國家、人物或組織。
3. keywords：選出 3～5 個最能代表新聞核心事件或議題的關鍵字，
   避免單純使用國家、人物、公司名稱作為關鍵字。。
新聞標題：
{title}
新聞內容：
{content}
"""

class NewsAnalysis(BaseModel):
    industry: list[str]
    companies: list[str]
    keywords: list[str]


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-3.5-flash-lite",
#     contents=prompt
# )


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": NewsAnalysis,
    }
)


# model="gemini-3.5-flash-lite"
# gemini-3.8-flash

print(response.text)


        
# %%
