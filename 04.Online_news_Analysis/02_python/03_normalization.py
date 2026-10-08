# %%
import pandas as pd
from sqlalchemy import create_engine, text


## 載入SQLraw_news資料
engine = create_engine("mysql+pymysql://root:123456@localhost/financial_news")

# 
df = pd.read_sql("""
    SELECT *
    FROM news_industry
""", engine)

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
# %%
