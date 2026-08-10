use practice;


-- 確認資料庫有那些表格，如果用count可只顯示數量
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_TYPE = 'BASE TABLE';

-- 簡易查看特定表格資料
select *
from raw_orders 
limit 10;





select customer_id , sum(amount) as total_amount
from orders
group by customer_id ;


-- 實施資料分析練習

with  month_01_order as (
	select customer_id , DATE_SUB(order_date ,interval DAY(order_date)-1 day) as order_month_01,
		product_id ,amount
	from orders
) 
select *
from month_01_order 
limit 20;