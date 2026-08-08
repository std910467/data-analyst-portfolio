-- 當資料庫出現重複資訊時，砍掉重練是選項，但資料筆數太多可以用清理
-- 先建立一張去重後的新表
-- 確認筆數正確
-- 再把舊表換掉
use olist;
-- 建立去重後的乾淨表，CTAS（Create Table As Select）
CREATE TABLE olist_order_items_dataset_clean AS
SELECT DISTINCT *
FROM olist_order_items_dataset;

-- 檢查內容是否已經沒有重複了，順便看數值是否是否合理
SELECT COUNT(*) AS data_rows
FROM olist_order_items_dataset_clean;



SELECT COUNT(*) AS clean_rows,
       COUNT(DISTINCT order_id , order_item_id ) AS distinct_key
FROM olist_order_items_dataset_clean;
-- 如果 clean_rows 和 distinct_key 數字一樣，表示資料沒重複了。

-- 確認沒問題後，再執行下面這段取代原表：
--  刪除有重複的舊表
DROP TABLE olist_order_items_dataset ;

-- 把乾淨的表改回原來的名字
RENAME TABLE olist_order_items_dataset_clean TO olist_order_items_dataset;
