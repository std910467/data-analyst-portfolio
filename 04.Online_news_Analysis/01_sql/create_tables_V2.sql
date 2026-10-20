CREATE DATABASE financial_news;
SHOW DATABASES;


USE financial_news;


-- 創造空表格，讓py輸入資料使用_V2
-- 先創造網路原始文章存放的空表格~V1已經做完
-- CREATE TABLE raw_news (
--     news_id      INT AUTO_INCREMENT PRIMARY KEY,
--     title 	VARCHAR(255) NOT null,
--     published_at   DATETIME  NOT NULL,
--     url    VARCHAR(255) NOT null,
--     content    text  NOT null,
-- 	clean_url VARCHAR(255) NOT NULL UNIQUE,
--     source	VARCHAR(25) NOT null
-- );

-- 創造LLM解析完存放的空表格_V2
CREATE TABLE news_industry_v2 (
    news_id INT NOT NULL,
    sub_industry VARCHAR(255) NOT NULL,
    main_industry VARCHAR(50) NOT NULL,
    UNIQUE (news_id, sub_industry, main_industry)
);

CREATE TABLE news_company_v2 (
    news_id      INT NOT null,
    company 	VARCHAR(255) NOT null,
    UNIQUE (news_id, company)
);

CREATE TABLE news_keyword_v2 (
    news_id      INT NOT null,
    keyword 	VARCHAR(255) NOT null,
    UNIQUE (news_id, keyword)
);


--刪除表格
drop table XXXXXXXXXXXXX ;




-- 搜尋特定字串，並計算數量
SELECT normalized_industry, COUNT(*) AS industry_count
FROM news_industry
WHERE normalized_industry LIKE '%半導體%'
GROUP BY normalized_industry
ORDER BY industry_count DESC;

查看同news_id裡面人工標準化內容是否有重複
SELECT
    news_id,
    normalized_industry,
    COUNT(*) AS cnt
FROM news_industry
GROUP BY news_id, normalized_industry
HAVING COUNT(*) > 1
ORDER BY cnt DESC, news_id;