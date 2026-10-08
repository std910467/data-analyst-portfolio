# %%
import pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum
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
class Industry(str, Enum):
    ENERGY = "能源"
    MATERIALS = "原物料"
    INDUSTRIALS = "工業"
    CONSUMER_DISCRETIONARY = "非必需消費"
    CONSUMER_STAPLES = "必需消費"
    HEALTH_CARE = "醫療保健"
    FINANCIALS = "金融"
    INFORMATION_TECHNOLOGY = "資訊科技"
    COMMUNICATION_SERVICES = "通訊服務"
    UTILITIES = "公用事業"
    REAL_ESTATE = "不動產"
    OTHER = "其他"

class IndustryItem(BaseModel):
    sub_industry: str
    main_industry: Industry

class NewsAnalysis(BaseModel):
    industries: list[IndustryItem]
    companies: list[str]
    keywords: list[str]

## 載入Gemini API，使用LLM模型
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

sql_industry = text("""
INSERT IGNORE INTO news_industry
(news_id, industry )
VALUES
(:news_id, :industry)
""")
sql_keyword = text("""
INSERT IGNORE INTO news_keyword
(news_id, keyword)
VALUES
(:news_id, :keyword)
""")
sql_company = text("""
INSERT IGNORE INTO news_company
(news_id, company)
VALUES
(:news_id, :company)
""")

print(f"Total news:{len(df)}")
insert_times = 0
for i, row in df.iterrows():
    news_id = row["news_id"]
    title = row["title"]
    content = row["content"]
    print(f"Processing news_id: {news_id}")
    ## 設定詢問的問題
    prompt = f"""
    請分析以下財經新聞。
    要求：
    1. industry：
        判斷新聞涉及的細分產業，可有多個。
        每個 sub_industry 都必須同時指定 main_industry。
        main_industry 必須從 Schema 允許的 GICS 大分類中選擇。
        若無法合理歸類，使用「其他」。
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
    for industry in response.parsed.industries:
        print(industry.sub_industry, "→", industry.main_industry.value)
    # try:
    #     with engine.begin() as conn:  
    #         for industry in response.parsed.industry:       
    #             conn.execute(sql_industry, {
    #                 "news_id": news_id,
    #                 "industry": industry
    #             })
    #         for company in response.parsed.companies:
    #             conn.execute(sql_company, {
    #                 "news_id": news_id,
    #                 "company": company
    #             })
    #         for keyword in response.parsed.keywords:
    #             conn.execute(sql_keyword, {
    #                 "news_id": news_id,
    #                 "keyword": keyword
    #             })
    # except Exception as e:
    #     print(f"news_id {news_id} insert SQL failed: {e}")
    #     continue
    insert_times +=1

print(f"Total news: {len(df)}")
print(f"Inserted: {insert_times} news")
# %%
