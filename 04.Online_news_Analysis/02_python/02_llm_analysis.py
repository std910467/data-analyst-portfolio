# %%
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv


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
請整理以下財經新聞的重點。
新聞標題：
{title}
新聞內容：
{content}
"""

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

# model="gemini-3.5-flash-lite"
# gemini-3.8-flash

print(response.text)


        
# %%
