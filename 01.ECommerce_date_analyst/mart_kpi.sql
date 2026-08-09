USE olist;

-- 確認表格裡面有哪些資料、以及資料型態，
select * from int_order_summary limit 5;
describe int_order_summary;
select distinct order_status from int_order_summary limit 10;

-- 計算一下dilivered已送達的，訂單已經完成的部分占多少
-- 送達率大約97%，後續資料都只針對dilivered的部分計算 
select 	count(*) , 
		count(case when order_status = "delivered" then 1 end) as delivered,
		round(count(case when order_status = "delivered" then 1 end)*1.0/count(*),2)
from int_order_summary ios ;	


-- mart_monthly_revenue
create table mart_monthly_revenue as 
with month_order as ( 
	select str_to_date(DATE_FORMAT(order_purchase_timestamp, "%Y-%m-01"), "%Y-%m-%d") as order_month,
			amount 
	from int_order_summary ios 
	where order_status = "delivered"
),
month_revenue as (
	select order_month , round(sum( amount),2) as revenue
	from month_order
	group by order_month 
),
month_revenue_prev as(
	select order_month , revenue,
			lag( revenue, 1) over (order by order_month ) as revenue_prev
	from month_revenue
),
month_revenue_prev_growth as(
	select * , ROUND( (revenue-revenue_prev)*1.0/revenue_prev,4) as growth_rate
	from month_revenue_prev 
)
select * from month_revenue_prev_growth  order by order_month
;

-- mart_customer_retention
-- mart_rfm_table