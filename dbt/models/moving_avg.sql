-- models/moving_avg.sql

with source_data as (
    select
    	time,
        asset_id_base,
        asset_id_quote,
        rate,
    from {{ ref('project_bitcoin') }}
),

moving_avg_calc as (
    select
    	time,
    	asset_id_base,
    	asset_id_quote,
        avg(rate) over (
            partition by id
            order by time
            rows between 2 preceding and current row
        ) as moving_avg_3
    from source_data
)

select * from moving_avg_calc
