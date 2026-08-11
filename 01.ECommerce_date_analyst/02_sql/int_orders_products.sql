use olist;

-- 測試一下，要加的表。
-- SELECT * FROM olist_order_items_dataset LIMIT 5;
-- SELECT * FROM olist_orders_dataset LIMIT 5;
-- SELECT * FROM olist_customers_dataset LIMIT 5;
-- SELECT * FROM olist_products_dataset LIMIT 5;
-- SELECT * FROM product_category_name_translation LIMIT 5;

-- 開始join 並篩選
-- drop table int_order_product;

CREATE TABLE int_order_product as
with order_amount as (
	select order_id , 
			product_id,
			round(price + freight_value ,2) as amount
	from olist_order_items_dataset 
	),
	order_data as (
		select ood.order_id  , ood.order_status  , ood.order_purchase_timestamp , oa.product_id , oa.amount   
		from olist_orders_dataset ood 
		left join order_amount as oa on ood.order_id = oa.order_id 
	),
	products_dataset as (
		select 	opd.product_id , 
			COALESCE(
        	NULLIF(TRIM(pcnt.product_category_name_english), ''),
        	'Uncategorized') as product_category
	from olist_products_dataset opd 
	left join product_category_name_translation pcnt 
	on opd.product_category_name = pcnt.product_category_name 
	)
select od.* , pd.product_category 
from order_data od
left join products_dataset pd  on od.product_id =pd.product_id;



SELECT * FROM int_order_product
LIMIT 5;

SELECT count(*) , count(distinct order_id   ), count(distinct product_category  ) 
FROM int_order_product;



