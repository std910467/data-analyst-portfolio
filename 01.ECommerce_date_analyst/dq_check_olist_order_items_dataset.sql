use olist;

-- 抽樣檢查
-- 隨機看 5 筆、資料筆數太多會很慢
-- SELECT * FROM olist_order_items_dataset
-- ORDER BY RAND()
-- LIMIT 5;
-- 看最新、最舊的資料
SELECT * FROM olist_order_items_dataset
-- ORDER BY 日期或是其他排序  desc 
LIMIT 5;


-- 檢查product_id 跟  order_id 有沒有 NULL
SELECT COUNT(*) AS total_rows,
       COUNT(product_id) AS non_null_product_id,
       COUNT(order_id) AS non_null_order_id,
       COUNT(*)*2 - COUNT(product_id)-COUNT(order_id) AS null_count
FROM olist_order_items_dataset;

-- 看看有沒有重複的、這按照olist設計，這表是複合主鍵order_id+order_item_id）
SELECT order_id, order_item_id ,COUNT(*) AS cnt
FROM olist_order_items_dataset
GROUP BY order_id , order_item_id
HAVING COUNT(*) >1
order by cnt  desc;


-- 檢查有沒有order_id,order_item_id前後有無空白
SELECT order_item_id,order_id
FROM olist_order_items_dataset
WHERE order_item_id <> TRIM(order_item_id) or order_id <> TRIM(order_id);

-- 總筆數
SELECT COUNT(*) FROM olist_order_items_dataset;

-- 日期正不正常，這邊用不到
-- SELECT MIN(order_purchase_timestamp), 
--        MAX(order_purchase_timestamp)
-- FROM 訂單表;
-- 
-- 金額有沒有異常（負數、過大），這邊用不到
-- SELECT MIN(amount), MAX(amount), AVG(amount)
-- FROM 訂單表;   