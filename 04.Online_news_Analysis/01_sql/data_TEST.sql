
SHOW DATABASES;


USE financial_news;


-- 先把目前 industry 的所有值及出現次數拉出來：
SELECT
    industry,
    COUNT(*) AS cnt
FROM news_industry
GROUP BY industry
ORDER BY cnt DESC;