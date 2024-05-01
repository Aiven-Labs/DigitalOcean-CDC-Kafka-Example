-- Create Table
CREATE TABLE public.sales
(
    productkey bigint,
    customerkey bigint,
    salesterritorykey bigint,
    salesordernumber varchar,
    totalproductcost double precision,
    salesamount double precision,
    id serial PRIMARY KEY,
    created_at timestamp
);

-- Create View
CREATE VIEW vw_sales AS
WITH timest AS (
    SELECT
        id,
        (LEFT(REPLACE(REPLACE(created_at::text, 'T', ' '), 'Z', ''), 23)::timestamp AT TIME ZONE 'America/New_York') - INTERVAL '4 hours' AS created_date
    FROM public.sales
)
SELECT
    s.*,
    t.created_date,
    CURRENT_TIMESTAMP AT TIME ZONE 'America/New_York' AS dt
FROM public.sales s
INNER JOIN timest t ON s.id = t.id;
