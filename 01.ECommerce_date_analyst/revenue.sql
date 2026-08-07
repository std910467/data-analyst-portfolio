USE olist;

select * from olist_orders_dataset  limit 5;

select 	count(*) as orders ,  
		count(case when order_status ='delivered' then 1 end ) as delivered,
		round(count(case when order_status ='delivered' then 1 end )*1.0/count(*) , 2) as delivered_rate
from olist_orders_dataset ;