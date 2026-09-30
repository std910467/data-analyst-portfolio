# %%
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

# 經濟日報
url = "https://money.udn.com/money/index"


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all(
    "a",attrs={"data-slotname": lambda x: x and "list_" in x})
news_list = []
for i, link in enumerate(links) :
    print(i)
    article_url = urljoin(url, link.get("href"))
    article_title = link.get("title")
    try:
        article_response = requests.get(article_url, timeout=10)
    except  requests.exceptions.RequestException:
        print(f"links[{i}] 連線失敗，跳過")
        continue
    article_soup = BeautifulSoup(
        article_response.text,"html.parser")
    article_time = article_soup.find("time")
    if article_time is None:
        article_time = None
    else : article_time = article_time.text.strip()
    article_body = article_soup.find("section", id="article_body")
    if article_body is None:
        print(f"links[{i}] 找不到資料，跳過")
        continue
    paragraphs = article_body.find_all("p", recursive=False)
    content_list = []
    for p in paragraphs:
        p_text = p.text.strip()
        if ( 
            p_text 
            and not p.find(class_="further-reading")
            and not p.find("a", attrs={"data-slotname": "list_文中延伸閱讀"})
            and not p.find(class_="ai_content_block")
            ):
            content_list.append(p_text )
    content = "\n".join(content_list)
    news_list.append({
        "title" : article_title,
        "published_at": article_time,
        "url" : article_url,
        "content" : content})
    
news_df = pd.DataFrame(news_list)
news_df["clean_url"] = news_df["url"].str.split("?").str[0]
news_df = news_df.drop_duplicates(
    subset="clean_url"
).reset_index(drop=True)
news_df["published_at"] = pd.to_datetime(
    news_df["published_at"])
news_df["source"] = "經濟日報"

# def insert_ignore(table, conn, keys, data_iter):
#     pass

#因為有設定唯一clean_url，所以一般insert遇到同資料會報錯，而且會停止輸入
#要用 IGNORE，但pandas套件沒直接支援。
sql = text("""
INSERT IGNORE INTO raw_news
(title, published_at, url, content, clean_url, source)
VALUES
(:title, :published_at, :url, :content, :clean_url, :source)
""")
data =  news_df.to_dict(orient="records")
with engine.begin() as conn:
    result = conn.execute(sql, data)
result.rowcount


        
# %%
