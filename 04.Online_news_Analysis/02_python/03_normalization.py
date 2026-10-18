# %%
import pandas as pd
from sqlalchemy import create_engine, text


## 載入SQLraw_news資料
engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

# 讀取產業資料，
df = pd.read_sql("""
    SELECT *
    FROM news_industry
""", engine)

#設定產業手動調整的map
industry_mapping = {
    "金融": "金融業"
}

df["normalized_industry"] = (
    df["industry"].map(industry_mapping).fillna(df["industry"])
)

df["normalized_industry"].value_counts().head(10)
df[df["industry"] != df["normalized_industry"]]
finance_df = df[
    df["industry"].isin(["金融", "金融業"])
]

finance_check = (
    finance_df
    .groupby("news_id")["industry"]
    .nunique()
)

finance_check = (
    finance_df
    .groupby("news_id")["industry"]
    .nunique()
)

finance_check[finance_check > 1]


# 比較V1、V2的分析的新聞是否一樣
df_v1 = pd.read_sql("""
    SELECT distinct news_id
    FROM news_keyword
    order by news_id
""", engine)
df_v2 = pd.read_sql("""
    SELECT distinct news_id
    FROM news_keyword_v2
    order by news_id
""", engine)
df_v1.equals(df_v2)
# %%
