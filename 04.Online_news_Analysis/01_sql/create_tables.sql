CREATE DATABASE financial_news;
SHOW DATABASES;


USE financial_news;


-- 創造空表格，讓py輸入資料使用

-- 先創造網路原始文章存放的空表格
CREATE TABLE raw_news (
    news_id      INT AUTO_INCREMENT PRIMARY KEY,
    title 	VARCHAR(255) NOT null,
    published_at   DATETIME  NOT NULL,
    url    VARCHAR(255) NOT null,
    content    text  NOT null,
	clean_url VARCHAR(255) NOT NULL UNIQUE,
    source	VARCHAR(25) NOT null
);

-- 先創造LLM解析完存放的空表格_V1
CREATE TABLE news_industry (
    news_id      INT NOT null,
    industry 	VARCHAR(255) NOT null,
    UNIQUE (news_id, industry)
);

CREATE TABLE news_company (
    news_id      INT NOT null,
    company 	VARCHAR(255) NOT null,
    UNIQUE (news_id, company)
);

CREATE TABLE news_keyword (
    news_id      INT NOT null,
    keyword 	VARCHAR(255) NOT null,
    UNIQUE (news_id, keyword)
);

-- 創造LLM解析完存放的空表格_V2版本
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
