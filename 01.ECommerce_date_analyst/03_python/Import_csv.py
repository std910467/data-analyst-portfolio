import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
# 檔案路徑
BASE_DIR = Path(__file__).resolve().parent
# 格式: mysql+pymysql://<帳號>:<密碼>@<主機>/<資料庫名稱>
engine = create_engine("mysql+pymysql://root:123456@localhost/olist")
csv_name= "olist_order_reviews_dataset.csv"
csv_file_path =BASE_DIR.parent / "01_raw_data"/csv_name

df = pd.read_csv(
    csv_file_path,
    encoding="utf-8",  # 若出現編碼錯誤可改 try 'utf-8-sig' 或 'latin1'
)
table_name = "olist_order_reviews_dataset"

df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",  # 如果有資料直接覆蓋重建
    index=False,
    chunksize=1000,  # 每 1000 筆寫入一次，確保穩定度
)