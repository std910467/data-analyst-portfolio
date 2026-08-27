use azure_pdm;


-- 測試一下，先確認表格內容。
SELECT * FROM pdm_errors
LIMIT 5; -- 告警時間、機器ID、告警原因
SELECT * FROM pdm_failures
LIMIT 5; -- 故障時間、機器ID、故障原因
SELECT * FROM pdm_machines
LIMIT 5; -- 機器ID、機器總類、使用年限
SELECT * FROM pdm_maint 
LIMIT 5; -- 維修時間、機器ID、維修或維護項目
SELECT * FROM pdm_telemetry 
LIMIT 10; -- 遙測資料 每小時1筆、電壓、轉速、壓力、震動

-- 檢查資料內容 
select min(datetime) , max(datetime) FROM pdm_telemetry; -- 資料涵蓋1年，但只到2016-01-01未足月，資料僅使用2015年
select min(datetime) , max(datetime) FROM pdm_maint; -- 維修資料是從2014-06-01開始到2016-01-01，為與其他同步資料故僅使用2015年


select distinct comp from pdm_maint ; -- 確認維修只有 comp1~4
select distinct failure from pdm_failures ; -- 確認故障只有 comp1~4
select distinct errorID from pdm_errors ; -- 確認告警只有 error1~5
 
-- 創造中間表格
CREATE TABLE int_daily_machine_summary as 
with daily_telemetry as (
	select 	date(datetime) as date ,
			machineID ,
			avg(volt) as d_volt,
			avg(rotate) as d_rotate,
			avg(pressure) as d_pressure,
			avg(vibration) as d_vibration
	from pdm_telemetry
	where datetime < '2016-01-01'
	group by DATE(datetime), machineID
	),
	daily_mach_telemetry as (
		select  dt.* , pm.model , pm.age
		from daily_telemetry as dt
		left join pdm_machines as pm on dt.machineID =pm.machineID 
	),
	daily_maint as (
		select  date(datetime) as date ,
				machineID ,
				count(case when comp='comp1' then 1 end) as comp1_times,
				count(case when comp='comp2' then 1 end) as comp2_times,
				count(case when comp='comp3' then 1 end) as comp3_times,
				count(case when comp='comp4' then 1 end) as comp4_times
		from pdm_maint 
		group by  date(datetime) ,machineID
	),
	daily_failures as (
		select	date(datetime) as date,
				machineID,
				count(case when failure='comp1' then 1 end) as comp1_failure,
				count(case when failure='comp2' then 1 end) as comp2_failure,
				count(case when failure='comp3' then 1 end) as comp3_failure,
				count(case when failure='comp4' then 1 end) as comp4_failure
		from pdm_failures
		group by date(datetime) ,machineID 	
	),
	daily_errors as (
		select	date(datetime) as date ,
				machineID ,
				count(case when errorID='error1' then 1 end) as error1_times,
				count(case when errorID='error2' then 1 end) as error2_times,
				count(case when errorID='error3' then 1 end) as error3_times,
				count(case when errorID='error4' then 1 end) as error4_times,
				count(case when errorID='error5' then 1 end) as error5_times
		from pdm_errors
		group by date(datetime) ,machineID 	
	)
	select 	dmt.* , 
			IFNULL(dm.comp1_times, 0) AS comp1_times,
    		IFNULL(dm.comp2_times, 0) AS comp2_times,
   		 	IFNULL(dm.comp3_times, 0) AS comp3_times,
    		IFNULL(dm.comp4_times, 0) AS comp4_times,
    		IFNULL(df.comp1_failure, 0) AS comp1_failure,
    		IFNULL(df.comp2_failure, 0) AS comp2_failure,
    		IFNULL(df.comp3_failure, 0) AS comp3_failure,
    		IFNULL(df.comp4_failure, 0) AS comp4_failure,
    		IFNULL(de.error1_times, 0) AS error1_times,
    		IFNULL(de.error2_times, 0) AS error2_times,
    		IFNULL(de.error3_times, 0) AS error3_times,
    		IFNULL(de.error4_times, 0) AS error4_times,
    		IFNULL(de.error5_times, 0) AS error5_times	
	from daily_mach_telemetry  as dmt
	left join daily_maint as dm on dmt.date = dm.date and dmt.machineID = dm.machineID
	left join daily_failures as df on dmt.date = df.date and dmt.machineID = df.machineID
	left join daily_errors as de on dmt.date = de.date and dmt.machineID = de.machineID
	order by dmt.date , dmt.machineID;

-- 檢查一下製作的表格狀況	
select *
from int_daily_machine_summary idms  
limit 20;

-- 檢查筆數
select count(*)
from int_daily_machine_summary; -- 100*365天=36500 無誤

-- 檢查有沒有 NULL
SELECT 
    SUM(d_volt IS NULL) ,
    SUM(d_rotate IS NULL) ,
    SUM(d_pressure IS NULL) ,
    SUM(d_vibration IS NULL) ,
    SUM(model IS NULL) ,
    SUM(age IS NULL) ,
    SUM(comp1_times IS NULL) ,
    SUM(comp2_times IS NULL) ,
    SUM(comp3_times IS NULL) ,
    SUM(comp4_times IS NULL) ,
    SUM(comp1_failure IS NULL) ,
    SUM(comp2_failure IS NULL) ,
    SUM(comp3_failure IS NULL) ,
    SUM(comp4_failure IS NULL) ,
    SUM(error1_times IS NULL) ,
    SUM(error2_times IS NULL) ,
    SUM(error3_times IS NULL) ,
    SUM(error4_times IS NULL) ,
    SUM(error5_times IS NULL)
FROM azure_pdm.int_daily_machine_summary;

