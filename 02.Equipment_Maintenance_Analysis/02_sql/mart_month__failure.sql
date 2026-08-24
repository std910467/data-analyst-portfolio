
use azure_pdm;

-- 測試一下，會使用到的表格內容。
select * from int_daily_machine_summary
limit 30;
-- 檢查資料內容 

-- 創造monthly x  model 資料
CREATE TABLE mart_monthly_model_failure as 
	select 	date(date_format(date,'%Y-%m-01')) as month,
			model,
			avg(d_volt) as y_volt,
			avg(d_rotate) as y_rotate,
			avg(d_pressure) as y_pressure,
			avg(d_vibration) as y_vibration,
			sum(comp1_times) as comp1_times, 
			sum(comp2_times) as comp2_times,
			sum(comp3_times) as comp3_times,
			sum(comp4_times) as comp4_times,
			sum(comp1_failure) as comp1_failure,
			sum(comp2_failure) as comp2_failure,
			sum(comp3_failure) as comp3_failure,
			sum(comp4_failure) as comp4_failure,
			sum(error1_times) as error1_times,
			sum(error2_times) as error2_times,
			sum(error3_times) as error3_times,
			sum(error4_times) as error4_times,
			sum(error5_times) as error5_times,
			SUM(comp1_failure + comp2_failure + comp3_failure + comp4_failure) as total_failures,
    		SUM(error1_times + error2_times + error3_times + error4_times + error5_times) as total_errors
	from int_daily_machine_summary
	group by date(date_format(date,'%Y-%m-01')),model
	order by month , model;

-- 檢查一下製作的表格狀況	
select *
from mart_monthly_model_failure
limit 20; -- 格式欄位正常

select count(*)
from mart_monthly_model_failure;-- 13個月*4種機型=52筆數正常

-- 故障筆數761無誤
select sum(total_failures)
from mart_monthly_model_failure;-- 本表故障筆數761
select count(*)
from pdm_failures ;-- 原始資料故障筆數761

-- 告警筆數3919無誤
select sum(total_errors)
from mart_monthly_model_failure;-- 告警筆數3919
select count(*)
from pdm_errors ;-- 告警筆數3919


