# %%
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI

engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

df = pd.read_sql(
    "SELECT * FROM raw_news",
    engine
)

title = df.loc[0, "title"]
content = df.loc[0, "content"]

print(title)
print(content)


        
# %%
