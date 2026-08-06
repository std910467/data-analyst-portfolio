CREATE DATABASE practice;
SHOW DATABASES;

USE practice;

--先創造對應的空表格
CREATE TABLE raw_orders  (
    order_id      INT PRIMARY KEY,
    customer_id   INT NOT NULL,
    product_id    INT NOT NULL,
    order_date    DATE NOT NULL,
    amount        DECIMAL(10,2) NOT NULL
);

-- 使用圖形界面將CSV匯入資料庫內

--計算資料筆數看有沒匯入成功
SELECT COUNT(*) FROM orders; 

--刪除表格
drop table raw_orders ;
