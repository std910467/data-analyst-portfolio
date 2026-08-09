use olist;

-- 抽樣檢查
-- 隨機~如果資料太多很耗時
-- SELECT * FROM olist_profucts_dataset
-- ORDER BY RAND()
-- LIMIT 5;
-- 或看最新、最舊的資料、這邊沒用

SELECT * FROM olist_products_dataset
LIMIT 10;


-- 檢查product_id 跟  product_category_name 有沒有 NULL
SELECT COUNT(*) AS total_rows,
       COUNT(product_id) AS non_null_product_id,
       COUNT(product_category_name) AS non_null_product_category_name,
       COUNT(*)*2 - COUNT(product_id)-COUNT(product_category_name) AS null_count
FROM olist_products_dataset;

-- 檢查product_id,product_category_name 有沒有空字串
SELECT product_id , product_category_name
FROM olist_products_dataset
WHERE TRIM(product_id)='' or TRIM(product_category_name)='';

-- 因為olist_products_dataset 的product_category_name 有空字串，預計填入Uncategorized



-- 看看有沒有重複的 product_id 
SELECT product_id , COUNT(*) AS cnt
FROM olist_products_dataset
GROUP BY product_id
HAVING COUNT(*) >1
order by cnt  desc;


-- 檢查有沒有product_id,product_category_name前後空白
SELECT product_id , product_category_name
FROM olist_products_dataset
WHERE product_id <> TRIM(product_id) or product_category_name <> TRIM(product_category_name);



-- 總筆數
SELECT COUNT(*) FROM olist_products_dataset;

-- 日期正不正常，這邊用不到
-- SELECT MIN(order_purchase_timestamp), 
--        MAX(order_purchase_timestamp)
-- FROM 訂單表;
-- 
-- 金額有沒有異常（負數、過大），這邊用不到
-- SELECT MIN(amount), MAX(amount), AVG(amount)
-- FROM 訂單表;   