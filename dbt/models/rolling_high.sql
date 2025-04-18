{{ config(materialized='view') }}

WITH
  last_60 AS (
    SELECT
      *
    FROM
      {{ source('public', 'project_bitcoin' }}
    ORDER BY
      time DESC
    LIMIT
      60
  ),
  ordered_last_60 AS (
    SELECT
      *
    FROM
      last_60
    ORDER BY
      time ASC
  ),
  moving_average AS (
    SELECT
      time,
      rate,
      AVG(rate) OVER (
        ORDER BY
          time ROWS BETWEEN 11 preceding
          AND CURRENT ROW
      )
    FROM
      ordered_last_60
  )
SELECT
  *
FROM
  moving_average;
