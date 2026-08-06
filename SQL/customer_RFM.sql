
--刪除表格
drop table if exist customer_RFM ;


create table customer_RFM as(
	select 	customer_id ,
			timestampdiff(day,max(order_date),current_date()) as R,
			count(*) as F,
			sum(amount) as M
	from raw_orders
	group by customer_id
	)