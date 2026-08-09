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


-- drop mart_monthly_revenue 如果要重做的話
DROP TABLE IF exists mart_monthly_revenue;
/*============================================
 create mart_monthly_revenue---營收
  ==============================================*/

-- create mart_monthly_revenue
create table mart_monthly_revenue as 
with month_order as ( 
	select str_to_date(DATE_FORMAT(order_purchase_timestamp, "%Y-%m-01"), "%Y-%m-%d") as order_month,
			amount 
	from int_order_summary ios 
	where 	order_status = "delivered"
			and order_purchase_timestamp >= '2017-01-01'
  			and order_purchase_timestamp <  '2018-09-01'
),
month_revenue as (
	select order_month , round(sum( amount),2) as revenue ,count(*) as orders
	from month_order
	group by order_month 
),
month_revenue_prev as(
	select order_month as month , revenue,
			lag( revenue, 1) over (order by order_month ) as revenue_prev,
			orders
	from month_revenue
),
month_revenue_prev_growth as(
	select * , ROUND( (revenue-revenue_prev)*1.0/revenue_prev,4) as growth_rate
	from month_revenue_prev 
)
select * from month_revenue_prev_growth  order by month
;

/*============================================
 create mart_monthly_retention---留存
  ==============================================*/

-- create mart_monthly_retention
create table mart_monthly_retention as 
with month_order_customer as ( 
	select 	str_to_date(DATE_FORMAT(order_purchase_timestamp, "%Y-%m-01"), "%Y-%m-%d") as order_month,
			customer_unique_id
	from int_order_summary
	where 	order_status = "delivered"
			and order_purchase_timestamp >= '2017-01-01'
  			and order_purchase_timestamp <  '2018-09-01'
),
customer_first as (
	select 	customer_unique_id,
			min(order_month) as first_month
	from month_order_customer
	group by customer_unique_id
),
customer_first_repeat as (
	select 	cf.* , 
			moc.order_month as repeat_month 
	from customer_first as cf
	left join month_order_customer moc
	on cf.customer_unique_id = moc.customer_unique_id 
	and cf.first_month < moc.order_month 
)
select 	first_month as month,
		count(distinct customer_unique_id ) as new_customers,
		count(distinct case when timestampdiff(month,first_month,repeat_month)=1 then  customer_unique_id end ) as repeat_1m_customers,
		count(distinct case when timestampdiff(month,first_month,repeat_month)=2 then  customer_unique_id end ) as repeat_2m_customers,
		count(distinct case when timestampdiff(month,first_month,repeat_month)=3 then  customer_unique_id end ) as repeat_3m_customers
from customer_first_repeat
group by first_month
order by month ;

/*============================================
 create mart_month_customer_segment---顧客分類
 考量資料日期是取至2018-09，計算R的時候用 2018-09-01
  ==============================================*/

-- create mart_month_customer_segment，因為根據上面資料來看 回購率過低(1%)，f看不出價值，僅評估R_M
create table mart_month_customer_segment as
with customer_order as (
	select 	str_to_date(DATE_FORMAT(order_purchase_timestamp, "%Y-%m-01"), "%Y-%m-%d") as order_month,
			order_purchase_timestamp ,
			customer_unique_id as customer,
			amount 
	from int_order_summary ios 
	where 	order_status = "delivered"
			and order_purchase_timestamp >= '2017-01-01'
  			and order_purchase_timestamp <  '2018-09-01'
),
customer_RFM as(
	select 	customer , 
			min(order_month) as first_order_month,
			-- DATEDIFF('2018-09-01', order_purchase_timestamp)
			timestampdiff(day ,DATE_FORMAT(max(order_purchase_timestamp), "%Y-%m-%d"),'2018-09-01') as R,
	 		count(*) as F,
	 		ROUND(SUM(amount), 2) as M 
	from customer_order
	group by customer
),
customer_RFM_Mrate as(
	select 	*,
			PERCENT_RANK() OVER (ORDER BY M DESC) AS M_rank_pct
	from customer_RFM 
),
customer_seg as(
	select *,
			case 	when R<180 and M_rank_pct <= 0.2 then '近期高價值客'
					when R>=180 and M_rank_pct <= 0.2 then '遠期高價值客'
					when R<180 and M_rank_pct > 0.2 then '近期大眾'
					else '遠期大眾' end as segment
	from customer_RFM_Mrate
)
select first_order_month as month, 
		count(case when segment = '近期高價值客' then 1 end ) as 近期高價值客,
		count(case when segment = '遠期高價值客' then 1 end ) as 遠期高價值客,
		count(case when segment = '近期大眾' then 1 end ) as 近期大眾,
		count(case when segment = '遠期大眾' then 1 end ) as 遠期大眾
from customer_seg 
group by first_order_month
order by month;
	
/*============================================
 create mart_month_product--產品
  ==============================================*/


create table mart_month_product as
with product_month as ( 
	select 	product_category,
			str_to_date(DATE_FORMAT(order_purchase_timestamp, "%Y-%m-01"), "%Y-%m-%d") as order_month,
			amount 
	from int_order_product
	where 	order_status = "delivered"
			and order_purchase_timestamp >= '2017-01-01'
  			and order_purchase_timestamp <  '2018-09-01'
	),
	product_sum as (
		select 	product_category , order_month , 
				sum(amount) as pro_revenue
		from product_month 
		group by product_category ,order_month
	),
	month_product as (
		select 	product_category , 
				order_month , 
				pro_revenue ,
				row_number() over (partition by order_month order by pro_revenue desc) as pro_revenue_row
		from product_sum
		order by order_month , pro_revenue_row
		)
select	order_month ,
		max(case when pro_revenue_row=1 then product_category end) as NO_1_product,
		max(case when pro_revenue_row=2 then product_category end) as NO_2_product,
		max(case when pro_revenue_row=3 then product_category end) as NO_3_product,
		round(sum(case when pro_revenue_row<=3 then pro_revenue end)*1.0/sum(pro_revenue),4) as NO1_3_revenue_rate
from month_product
group by order_month 
order by order_month ;

	
	