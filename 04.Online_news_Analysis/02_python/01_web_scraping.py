# %%
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

news_df.to_sql(
    name="raw_news",
    con=engine,
    if_exists="append",
    method=IGNORE,
    index=False
)
df = pd.read_sql(
    "SELECT * FROM raw_news",
    engine
)
cursor = conn.cursor()

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
        text = p.text.strip()
        if ( 
            text
            and not p.find(class_="further-reading")
            and not p.find("a", attrs={"data-slotname": "list_文中延伸閱讀"})
            and not p.find(class_="ai_content_block")
            ):
            content_list.append(text)
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




## 下面指令測試用
news_df["title"].str.len().max()
news_df["url"].str.len().max()
news_df["clean_url"].str.len().max()
news_df["content"].str.len().max()

links[22]
print(article_url)
print(article_url)

article_time.text.strip()
print(article_time)
print()




article_url = links[0].get("href")
article_title = links[0].get("title")


test_response = requests.get(
    "https://money.udn.com/money/get_article/4/1001/5591/11162?_=1790600658361",
    timeout=10
)

print(test_response.status_code)
print(test_response.text[:1000])


article_soup = BeautifulSoup(
    article_response.text,"html.parser")
article_body = article_soup.find("section", id="article_body")

paragraphs = article_body.find_all("p", recursive=False)
content_list = []

for p in paragraphs:
    text = p.text.strip()

    if (
        text
        and not p.find(class_="further-reading")
        and not p.find("a", attrs={"data-slotname": "list_文中延伸閱讀"})
        and not p.find(class_="ai_content_block")
    ):
        content_list.append(text)
content = "\n".join(content_list)

print(article_title)
print(article_url)
print(content)

df = pd.DataFrame([{
    "title": article_title,
    "url": article_url,
    "content": content
}])


print(df)
        
# %%
