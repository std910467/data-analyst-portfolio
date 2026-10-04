# %%
import pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import time

## 載入SQLraw_news資料
engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

# 讀取尚未進行 LLM 分析的新聞，排除已存在於 news_keyword 的 news_id
df = pd.read_sql("""
    SELECT r.*
    FROM raw_news r
    WHERE NOT EXISTS (
        SELECT *
        FROM news_keyword k
        WHERE k.news_id = r.news_id
)
""", engine)
## 設定LLM輸出的格式
class NewsAnalysis(BaseModel):
    industry: list[str]
    companies: list[str]
    keywords: list[str]

## 載入Gemini API，使用LLM模型
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

industry_list = []
company_list = []
keyword_list = []
print(f"Total news:{len(df)}")

for i, row in df.iterrows():
    news_id = row["news_id"]
    title = row["title"]
    content = row["content"]
    print(f"Processing news_id: {news_id}")
    ## 設定詢問的問題
    prompt = f"""
    請分析以下財經新聞。
    要求：
    1. industry：判斷新聞涉及的產業，可有多個。
    2. companies：列出新聞涉及的公司，只包含企業，不包含政府、國家、人物或組織。
    3. keywords：選出 3～5 個最能代表新聞核心事件或議題的關鍵字，
    避免單純使用國家、人物、公司名稱作為關鍵字。
    新聞標題：
    {title}
    新聞內容：
    {content}
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": NewsAnalysis,
            }
        )

    # 避免LLM 頻繁詢問出錯，每次問完間隔5秒
# model="gemini-3.5-flash-lite"
# model="gemini-3.8-flash"
    except Exception as e:
        print(f"news_id {news_id} failed: {e}")
        continue
    finally:
        time.sleep(5)   
        
    for industry in response.parsed.industry:
        industry_list.append({
            "news_id": news_id,
            "industry": industry
        })
    for company in response.parsed.companies:
        company_list.append({
            "news_id": news_id,
            "company": company
        })
    for keyword in response.parsed.keywords:
        keyword_list.append({
            "news_id": news_id,
            "keyword": keyword
        })

#因為有設定唯一(new_id,XXXX)，所以一般insert遇到同資料會報錯，而且會停止輸入
#要用 IGNORE，但pandas套件沒直接支援。
sql = text("""
INSERT IGNORE INTO news_industry
(news_id, industry )
VALUES
(:news_id, :industry)
""")
# data =  news_df.to_dict(orient="records")
with engine.begin() as conn:
    result = conn.execute(sql, industry_list)
print(f"industry fetched {len(industry_list)} records.")
print(f"industry inserted {result.rowcount} new records.")

sql = text("""
INSERT IGNORE INTO news_keyword
(news_id, keyword)
VALUES
(:news_id, :keyword)
""")
with engine.begin() as conn:
    result = conn.execute(sql, keyword_list)
print(f"keyword fetched {len(keyword_list)} records.")
print(f"keyword inserted {result.rowcount} new records.")

sql = text("""
INSERT IGNORE INTO news_company
(news_id, company)
VALUES
(:news_id, :company)
""")
with engine.begin() as conn:
    result = conn.execute(sql, company_list)
print(f"company fetched {len(company_list)} records.")
print(f"company inserted {result.rowcount} new records.")


# 下面是測試用的指令
tables = pd.read_sql("SHOW TABLES", engine)
print(tables)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": NewsAnalysis,
    }
)
response.parsed

# model="gemini-3.5-flash-lite"
# model="gemini-3.8-flash"
industry_list=[]
print(response.text)
print(response.parsed)
response.text[10]
response.parsed.industry

industry.append(response.parsed.industry)
news_id=1
for industry in response.parsed.industry:
    industry_list.append({
        "news_id": news_id,
        "industry": industry
    })
industry_df = pd.DataFrame(industry_list)
print(industry_df)

print(response.parsed.industry)
print(response.parsed.companies)
print(response.parsed.keywords)
# %%
