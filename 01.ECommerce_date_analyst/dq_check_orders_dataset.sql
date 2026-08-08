use olist;

-- 抽樣檢查
-- 隨機看 5 筆
SELECT * FROM olist_orders_dataset
ORDER BY RAND()
LIMIT 5;
-- 或看最新、最舊的資料、這邊沒用
-- SQLSELECT * FROM 你的訂單表
-- ORDER BY 日期或是其他排序  desc 
-- LIMIT 10;


-- 檢查customer_id 跟  order_id 有沒有 NULL
SELECT COUNT(*) AS total_rows,
       COUNT(customer_id) AS non_null_customer_id,
       COUNT(order_id) AS non_null_order_id,
       COUNT(*)*2 - COUNT(customer_id)-COUNT(order_id) AS null_count
FROM olist_orders_dataset;

-- 看看有沒有重複的 customer_id（按照olist設計，一個訂單對應一個customer_id ，正常不應該重複）
SELECT order_id, COUNT(*) AS cnt
FROM olist_orders_dataset
GROUP BY order_id
HAVING COUNT(*) >1
order by cnt  desc;


-- 檢查有沒有customer_id,order_id前後空白
SELECT customer_id,order_id
FROM olist_orders_dataset
WHERE customer_id <> TRIM(customer_id) or order_id <> TRIM(order_id);

-- 總筆數
SELECT COUNT(*) FROM olist_orders_dataset;

-- 日期正不正常，這邊用不到
-- SELECT MIN(order_purchase_timestamp), 
--        MAX(order_purchase_timestamp)
-- FROM 訂單表;
-- 
-- 金額有沒有異常（負數、過大），這邊用不到
-- SELECT MIN(amount), MAX(amount), AVG(amount)
-- FROM 訂單表;   