
CREATE DATABASE olist;
SHOW DATABASES;

USE olist;

-- 使用圖形界面將CSV匯入資料庫內、使用DBeaver有部分筆數匯入失敗先skip
-- 發現是 olist_order_reviews_dataset因為評論太長，超過預設的255 所以要
-- 先看一下格式
DESCRIBE olist_order_reviews_dataset;
-- 變更欄位格式
ALTER TABLE olist_order_reviews_dataset
MODIFY COLUMN review_id VARCHAR(100),
MODIFY COLUMN order_id VARCHAR(100),
MODIFY COLUMN review_comment_message TEXT;
-- 清空olist_order_reviews_dataset資料

TRUNCATE TABLE olist_order_reviews_dataset;
TRUNCATE TABLE olist_customers_dataset;


-- 結論用DBeaver匯入失敗，欄位長度好了，但評論欄的資料有ENTER換行，DBeaver 的 CSV 匯入器誤把留言裡的「換行」當成下一筆資料的開始，導致整筆資料發生「大錯位」
-- 建議用Pandas匯入


-- 計算資料筆數看有沒匯入成功
SELECT COUNT(*) FROM olist_customers_dataset;
SELECT COUNT(*) FROM olist_geolocation_dataset; 
SELECT COUNT(*) FROM olist_order_items_dataset;
SELECT COUNT(*) FROM olist_order_payments_dataset;
SELECT COUNT(*) FROM olist_order_reviews_dataset;
SELECT COUNT(*) FROM olist_orders_dataset;
SELECT COUNT(*) FROM olist_products_dataset;
SELECT COUNT(*) FROM olist_sellers_dataset;
SELECT COUNT(*) FROM product_category_name_translation;


-- 刪除表格
drop table raw_orders ;
