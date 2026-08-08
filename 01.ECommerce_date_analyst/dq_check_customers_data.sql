use olist;

-- 抽樣檢查
-- 隨機看 5筆
SELECT * FROM olist_customers_dataset
ORDER BY RAND()
LIMIT 5;
-- 或看最新、最舊的資料、這邊沒用
-- SQLSELECT * FROM 你的訂單表
-- ORDER BY 日期或是其他排序  desc 
-- LIMIT 10;


-- 檢查customer_id 跟  customer_unique_id 有沒有 NULL
SELECT COUNT(*) AS total_rows,
       COUNT(customer_id) AS non_null_customer_id,
       COUNT(customer_unique_id) AS non_null_customer_unique_id,
       COUNT(*)*2 - COUNT(customer_id)-COUNT(customer_unique_id) AS null_count
FROM olist_customers_dataset;

-- 看看有沒有重複的 customer_id（按照olist設計，一個訂單對應一個customer_id ，正常不應該重複）
SELECT customer_id, COUNT(*) AS cnt
FROM olist_customers_dataset
GROUP BY customer_id
HAVING COUNT(*) >1
order by cnt  desc;

-- 順便看一下  customer_unigue_id（按照olist設計，customer_unique_id正常可以對應多張訂單，也就是可以對應多個customer_id）
SELECT customer_unique_id, COUNT(*) AS cnt
FROM olist_customers_dataset
GROUP BY customer_unique_id
HAVING COUNT(*) >1
order by cnt  desc;


-- 檢查有沒有customer_id,customer_unique_id前後空白
SELECT customer_id,customer_unique_id
FROM olist_customers_dataset
WHERE customer_id <> TRIM(customer_id) or customer_unique_id <> TRIM(customer_unique_id);

-- 總筆數
SELECT COUNT(*) FROM olist_customers_dataset;

-- 日期正不正常，這邊用不到
-- SELECT MIN(order_purchase_timestamp), 
--        MAX(order_purchase_timestamp)
-- FROM 訂單表;
-- 
-- 金額有沒有異常（負數、過大），這邊用不到
-- SELECT MIN(amount), MAX(amount), AVG(amount)
-- FROM 訂單表;   