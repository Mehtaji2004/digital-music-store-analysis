-- ==============================================================================
-- 03: ADVANCED ANALYTICS (WINDOW FUNCTIONS, CTES & TIME SERIES)
-- Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)
-- Focus: RANK(), DENSE_RANK(), ROW_NUMBER(), LEAD(), LAG(), SUM() OVER(), NTILE()
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Q1: Cumulative Running Revenue and Order Velocity Over Time
-- Objective: Track financial traction by charting monthly revenue alongside a running total.
-- Concepts: DATE formatting, CTEs, Window Function: SUM() OVER (ORDER BY ...)
-- ------------------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT
        STRFTIME('%Y-%m', invoice_date) AS sales_month,
        COUNT(invoice_id) AS order_count,
        ROUND(SUM(total), 2) AS monthly_revenue
    FROM invoices
    GROUP BY STRFTIME('%Y-%m', invoice_date)
)
SELECT
    sales_month,
    order_count,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY sales_month), 2) AS cumulative_revenue,
    ROUND(AVG(monthly_revenue) OVER (ORDER BY sales_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS rolling_3mo_avg_revenue
FROM MonthlySales
ORDER BY sales_month ASC;


-- ------------------------------------------------------------------------------
-- Q2: Month-over-Month (MoM) Revenue Growth Rate
-- Objective: Determine momentum and revenue volatility across consecutive months.
-- Concepts: LAG(), Window Functions, Percentage calculation, CASE WHEN (division by zero)
-- ------------------------------------------------------------------------------
WITH MonthlySummary AS (
    SELECT
        STRFTIME('%Y-%m', invoice_date) AS sales_month,
        ROUND(SUM(total), 2) AS monthly_revenue
    FROM invoices
    GROUP BY STRFTIME('%Y-%m', invoice_date)
),
SalesWithLag AS (
    SELECT
        sales_month,
        monthly_revenue,
        LAG(monthly_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue
    FROM MonthlySummary
)
SELECT
    sales_month,
    monthly_revenue,
    COALESCE(prev_month_revenue, 0.0) AS previous_month_revenue,
    ROUND(monthly_revenue - COALESCE(prev_month_revenue, 0.0), 2) AS mom_dollar_change,
    CASE
        WHEN prev_month_revenue IS NULL THEN 0.0
        ELSE ROUND(((monthly_revenue - prev_month_revenue) / prev_month_revenue) * 100.0, 2)
    END AS mom_growth_pct
FROM SalesWithLag
ORDER BY sales_month ASC;


-- ------------------------------------------------------------------------------
-- Q3: Top 2 Best-Selling Tracks per Genre (Partitioned Ranking)
-- Objective: Curate genre-specific landing pages and highlight top performers.
-- Concepts: DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...), Multi-table CTE
-- ------------------------------------------------------------------------------
WITH TrackSalesByGenre AS (
    SELECT
        g.genre_id,
        g.name AS genre_name,
        t.track_id,
        t.name AS track_name,
        ar.name AS artist_name,
        COUNT(ii.invoice_line_id) AS units_sold,
        ROUND(SUM(ii.unit_price * ii.quantity), 2) AS track_revenue
    FROM genres g
    JOIN tracks t ON g.genre_id = t.genre_id
    JOIN albums al ON t.album_id = al.album_id
    JOIN artists ar ON al.artist_id = ar.artist_id
    JOIN invoice_items ii ON t.track_id = ii.track_id
    GROUP BY g.genre_id, g.name, t.track_id, t.name, ar.name
),
RankedTracks AS (
    SELECT
        genre_name,
        track_name,
        artist_name,
        units_sold,
        track_revenue,
        DENSE_RANK() OVER (PARTITION BY genre_name ORDER BY units_sold DESC, track_revenue DESC) AS genre_rank
    FROM TrackSalesByGenre
)
SELECT
    genre_name,
    genre_rank,
    track_name,
    artist_name,
    units_sold,
    track_revenue
FROM RankedTracks
WHERE genre_rank <= 2
ORDER BY genre_name ASC, genre_rank ASC, track_revenue DESC;


-- ------------------------------------------------------------------------------
-- Q4: Customer Lifetime Value (LTV) Quartile Distribution
-- Objective: Segment the customer base into 4 spend tiers (VIP, Tier 2, Tier 3, Low).
-- Concepts: NTILE(4) Window Function, Subqueries, Segment Aggregation
-- ------------------------------------------------------------------------------
WITH CustomerLTV AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.country,
        COUNT(i.invoice_id) AS total_orders,
        ROUND(SUM(i.total), 2) AS total_spend,
        NTILE(4) OVER (ORDER BY SUM(i.total) DESC) AS ltv_quartile
    FROM customers c
    JOIN invoices i ON c.customer_id = i.customer_id
    GROUP BY c.customer_id, customer_name, c.country
)
SELECT
    CASE ltv_quartile
        WHEN 1 THEN 'Tier 1 - VIP High Spenders (Top 25%)'
        WHEN 2 THEN 'Tier 2 - Above Average Spenders'
        WHEN 3 THEN 'Tier 3 - Moderate Spenders'
        WHEN 4 THEN 'Tier 4 - Entry-Level Spenders'
    END AS customer_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(MIN(total_spend), 2) AS min_spend_in_tier,
    ROUND(MAX(total_spend), 2) AS max_spend_in_tier,
    ROUND(AVG(total_spend), 2) AS avg_spend_in_tier,
    ROUND(SUM(total_spend), 2) AS tier_total_revenue,
    ROUND(SUM(total_spend) * 100.0 / (SELECT SUM(total) FROM invoices), 1) AS pct_of_store_revenue
FROM CustomerLTV
GROUP BY ltv_quartile
ORDER BY ltv_quartile ASC;


-- ------------------------------------------------------------------------------
-- Q5: Days Since Last Purchase & Churn Risk Analysis
-- Objective: Identify inactive customers who have lapsed beyond 180 days since their last order.
-- Concepts: JULIANDAY(), MAX() Date aggregation, CASE WHEN, Filtering
-- ------------------------------------------------------------------------------
WITH CustomerRecency AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.email,
        c.country,
        MAX(i.invoice_date) AS last_purchase_date,
        COUNT(i.invoice_id) AS order_count,
        ROUND(SUM(i.total), 2) AS total_spend,
        ROUND(JULIANDAY('2026-11-21') - JULIANDAY(MAX(i.invoice_date)), 0) AS days_since_last_purchase
    FROM customers c
    LEFT JOIN invoices i ON c.customer_id = i.customer_id
    GROUP BY c.customer_id, customer_name, c.email, c.country
)
SELECT
    customer_id,
    customer_name,
    country,
    last_purchase_date,
    days_since_last_purchase,
    order_count,
    total_spend,
    CASE
        WHEN days_since_last_purchase <= 60 THEN 'Active (0-60 days)'
        WHEN days_since_last_purchase BETWEEN 61 AND 180 THEN 'Warm (61-180 days)'
        ELSE 'Churn Risk (>180 days)'
    END AS retention_status
FROM CustomerRecency
ORDER BY days_since_last_purchase DESC;
