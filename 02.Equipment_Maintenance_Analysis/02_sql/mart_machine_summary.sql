use azure_pdm;


-- 測試一下，會使用到的表格內容。
select * from int_daily_machine_summary
limit 30;

-- 創造機器的綜整表
CREATE TABLE mart_machine_summary as 
	select 	machineID ,model,age,
			avg(d_volt) as avg_volt,
			avg(d_rotate) as avg_rotate,
			avg(d_pressure) as avg_pressure,
			avg(d_vibration) as avg_vibration,
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
    		SUM(error1_times + error2_times + error3_times + error4_times + error5_times) as total_errors,
    		SUM(comp1_times + comp2_times + comp3_times + comp4_times) as total_maint
	from int_daily_machine_summary
	group by machineID,model,age;

-- 檢查一下製作的表格狀況	
select *
from mart_machine_summary
limit 20; -- 格式欄位正常

select count(*)
from mart_machine_summary;-- 機器筆數100筆、正常

-- 故障筆數761 無誤
select sum(total_failures)
from mart_machine_summary;-- 本表故障筆數761
select count(*)
from pdm_failures 
where datetime>='2015-01-01' and datetime<'2016-01-01' ;-- 原始資料故障筆數761

-- 告警筆數3919 無誤
select sum(total_errors)
from mart_machine_summary;-- 告警筆數3917
select count(*)
from pdm_errors
where datetime>='2015-01-01' and datetime<'2016-01-01' ;-- 原始資料告警筆數3917

-- 維修筆數2879 無誤
select sum(total_maint)
from mart_machine_summary;-- 維修筆數2879
select count(*)
from pdm_maint
where datetime>='2015-01-01' and datetime<'2016-01-01' ;-- 原始資料維修筆數2879

