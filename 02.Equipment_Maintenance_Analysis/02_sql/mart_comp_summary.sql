
use azure_pdm;

-- 測試一下，會使用到的表格內容。
select * from int_daily_machine_summary
limit 30;

-- 創造monthly x  model 資料
CREATE TABLE mart_comp_summary as (
SELECT 'comp1' AS component,
       sum(comp1_failure) as failure,
       sum(comp1_times) as maint
FROM int_daily_machine_summary
UNION ALL
SELECT 'comp2',
       sum(comp2_failure),
       sum(comp2_times )
FROM int_daily_machine_summary
UNION ALL
SELECT 'comp3',
       sum(comp3_failure),
       sum(comp3_times )
FROM int_daily_machine_summary
UNION ALL
SELECT 'comp4',
       sum(comp4_failure),
       sum(comp4_times )
FROM int_daily_machine_summary	
);

-- 檢查一下製作的表格狀況	
select *
from mart_comp_summary
limit 20; -- 格式欄位正常

select count(*)
from mart_monthly_model_failure;-- 12個月*4種機型=48筆數正常

-- 故障筆數761無誤
select sum(total_failures)
from mart_monthly_model_failure;-- 本表故障筆數761
select count(*)
from pdm_failures 
where datetime>='2015-01-01' and datetime<'2016-01-01';-- 原始資料故障筆數761

-- 告警筆數3919無誤
select sum(total_errors)
from mart_monthly_model_failure;-- 告警筆數3917
select count(*)
from pdm_errors 
where datetime>='2015-01-01' and datetime<'2016-01-01';-- 告警筆數3917

-- 維修筆數
select sum(total_maint)
from mart_monthly_model_failure;-- 維修筆數2879
select count(*)
from pdm_maint 
where datetime>='2015-01-01' and datetime<'2016-01-01';-- 告警筆數28793279

