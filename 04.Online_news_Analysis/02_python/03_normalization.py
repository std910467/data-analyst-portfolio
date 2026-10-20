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
    **{k: "金融業" for k in ["金融"]},
    **{k: "科技業" for k in ["科技"]},
    **{k: "半導體" for k in ["半導體產業", "半導體業","半導體與電子業",
                          "半導體與關鍵礦產","半導體設備製造","半導體封測"]},
    **{k: "能源業" for k in ["能源", "能源產業"]},
    **{k: "人工智慧" for k in ["人工智慧產業", "人工智慧業", "人工智慧伺服器"]},
    **{k: "政府與公共事務" for k in ["政府與公共行政", "公共行政",
                            "政府公共行政","外交與公共事務",
                            "政治與公共事務","公共治理","公共政策"]},
    **{k: "保險業" for k in ["金融保險", "金融保險業", "醫療保險","保險"]},
    **{k: "物流業" for k in ["航運物流", "物流", "物流與供應鏈"]},
    **{k: "生技醫療" for k in ["生技製藥", "醫療與生技", "生技醫療產業","生技"]},  
}

# 依據df["industry"]使用map，填入normalized_industry，未在map的使用
df["normalized_industry"] = (
    df["industry"].map(industry_mapping).fillna(df["industry"])
)

#查看後狀況
df["normalized_industry"].value_counts().head(10)
#計算替換了多少
df[df["industry"] != df["normalized_industry"]].count()

#計算一下沒有替換的，狀況
df[df["industry"] == df["normalized_industry"]]["industry"].value_counts()

# 將人工標準化結果回填至 MySQL
sql_update = text("""
    UPDATE news_industry
    SET normalized_industry = :normalized_industry
    WHERE news_id = :news_id
      AND industry = :industry
""")

with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(sql_update, {
            "news_id": int(row["news_id"]),
            "industry": row["industry"],
            "normalized_industry": row["normalized_industry"]
        })

print(f"回填完成，共處理 {len(df)} 筆資料")

# %%
