use olist;

-- 測試一下，要加的表。
SELECT * FROM olist_order_items_dataset
LIMIT 5;
SELECT * FROM olist_orders_dataset
LIMIT 5;
SELECT * FROM olist_customers_dataset
LIMIT 5;


-- 開始join 並篩選
-- 目標 order_id , amount
select order_id , sum(price)+sum(freight_value) as amount
from olist_order_items_dataset
group by order_id 
limit 20;

CREATE TABLE int_order_summary as 
with order_amount as (
	select order_id , sum(price)+sum(freight_value) as amount
	from olist_order_items_dataset
	group by order_id 
	),
	order_data as (
		select ood.order_id  , ood.customer_id , ood.order_status  , ood.order_purchase_timestamp, oa.amount   
		from olist_orders_dataset ood 
		left join order_amount as oa on ood.order_id = oa.order_id 
	),
	order_customers as (
		select od.order_id ,od.amount ,od.order_purchase_timestamp ,od.order_status , ocd.customer_unique_id 
		from order_data od
		left join olist_customers_dataset ocd  on od.customer_id =ocd.customer_id 
	)
select *
from order_customers;


SELECT * FROM int_order_summary
LIMIT 5;

SELECT count(*) FROM int_order_summary
LIMIT 5;

