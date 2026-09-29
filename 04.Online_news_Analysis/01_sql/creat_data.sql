CREATE DATABASE financial_news;
SHOW DATABASES;


USE financial_news;

-- 創造空表格，讓py輸入資料使用

-- 先創造對應的空表格
CREATE TABLE raw_news (
    news_id      INT AUTO_INCREMENT PRIMARY KEY,
    title 	VARCHAR(255) NOT null,
    published_at   DATETIME  NOT NULL,
    url    VARCHAR(255) NOT null,
    content    text  NOT null,
	clean_url VARCHAR(255) NOT NULL UNIQUE,
    source	VARCHAR(25) NOT null
);

-- 看一下內容~一開始應該是空的
SELECT *
FROM raw_news;
--刪除表格
drop table raw_orders ;
