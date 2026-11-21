-- ==============================================================================
-- 02: SALES & REVENUE METRICS (BUSINESS INTELLIGENCE)
-- Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)
-- Focus: Multi-table relational joins, Revenue aggregation, Subqueries, CASE
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Q1: Top 10 Best-Selling Artists by Gross Revenue
-- Objective: Rank musical artists by actual cash revenue generated from track sales.
-- Concepts: Multi-table JOIN (artists -> albums -> tracks -> invoice_items), SUM()
-- ------------------------------------------------------------------------------
SELECT
    ar.artist_id,
    ar.name AS artist_name,
    COUNT(ii.invoice_line_id) AS tracks_sold,
    ROUND(SUM(ii.unit_price * ii.quantity), 2) AS total_revenue,
    ROUND(SUM(ii.unit_price * ii.quantity) * 100.0 / (SELECT SUM(unit_price * quantity) FROM invoice_items), 2) AS revenue_share_pct
FROM artists ar
JOIN albums al ON ar.artist_id = al.artist_id
JOIN tracks t ON al.album_id = t.album_id
JOIN invoice_items ii ON t.track_id = ii.track_id
GROUP BY ar.artist_id, ar.name
ORDER BY total_revenue DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- Q2: Geographic Market Performance (Revenue, Orders, and AOV)
-- Objective: Evaluate revenue and Average Order Value (AOV) across countries.
-- Concepts: GROUP BY, COUNT(DISTINCT), SUM(), AVG(), Derived Metrics
-- ------------------------------------------------------------------------------
SELECT
    billing_country,
    COUNT(DISTINCT invoice_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total), 2) AS total_sales,
    ROUND(AVG(total), 2) AS average_order_value,
    ROUND(SUM(total) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM invoices
GROUP BY billing_country
ORDER BY total_sales DESC;


-- ------------------------------------------------------------------------------
-- Q3: Sales Support Agent Performance Leaderboard
-- Objective: Compare support representatives on assigned customer revenue,
--            portfolio size, and conversion health.
-- Concepts: LEFT JOIN (employees -> customers -> invoices), Self-joins/hierarchies
-- ------------------------------------------------------------------------------
SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name AS sales_rep,
    e.title,
    e.hire_date,
    COUNT(DISTINCT c.customer_id) AS assigned_customers,
    COUNT(DISTINCT i.invoice_id) AS total_invoices_closed,
    ROUND(COALESCE(SUM(i.total), 0.0), 2) AS total_revenue_generated,
    ROUND(COALESCE(SUM(i.total), 0.0) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2) AS revenue_per_assigned_customer
FROM employees e
LEFT JOIN customers c ON e.employee_id = c.support_rep_id
LEFT JOIN invoices i ON c.customer_id = i.customer_id
WHERE e.title LIKE '%Sales%'
GROUP BY e.employee_id, e.first_name, e.last_name, e.title, e.hire_date
ORDER BY total_revenue_generated DESC;


-- ------------------------------------------------------------------------------
-- Q4: Most Popular Genre in Each Country
-- Objective: Identify customer taste variations by country to inform localized promotions.
-- Concepts: CTE (Common Table Expression), Nested Aggregations, GROUP BY
-- ------------------------------------------------------------------------------
WITH CountryGenreSales AS (
    SELECT
        c.country,
        g.name AS genre_name,
        COUNT(ii.invoice_line_id) AS units_purchased,
        ROUND(SUM(ii.unit_price * ii.quantity), 2) AS genre_revenue
    FROM customers c
    JOIN invoices i ON c.customer_id = i.customer_id
    JOIN invoice_items ii ON i.invoice_id = ii.invoice_id
    JOIN tracks t ON ii.track_id = t.track_id
    JOIN genres g ON t.genre_id = g.genre_id
    GROUP BY c.country, g.name
),
MaxGenrePerCountry AS (
    SELECT
        country,
        MAX(units_purchased) AS max_units
    FROM CountryGenreSales
    GROUP BY country
)
SELECT
    cgs.country,
    cgs.genre_name AS top_genre,
    cgs.units_purchased,
    cgs.genre_revenue
FROM CountryGenreSales cgs
JOIN MaxGenrePerCountry mg ON cgs.country = mg.country AND cgs.units_purchased = mg.max_units
ORDER BY cgs.units_purchased DESC, cgs.country ASC;


-- ------------------------------------------------------------------------------
-- Q5: Customer Cohort Purchase Frequency (Repeat vs One-Time Buyers)
-- Objective: Measure customer retention rate and repeat purchase behavior.
-- Concepts: Subqueries, CASE WHEN, Conditional Aggregation
-- ------------------------------------------------------------------------------
SELECT
    purchase_frequency_bracket,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct_of_customer_base,
    ROUND(SUM(lifetime_spend), 2) AS total_spend_bracket,
    ROUND(AVG(lifetime_spend), 2) AS avg_spend_per_customer
FROM (
    SELECT
        c.customer_id,
        COUNT(i.invoice_id) AS order_count,
        SUM(i.total) AS lifetime_spend,
        CASE
            WHEN COUNT(i.invoice_id) = 1 THEN '1. One-Time Buyer'
            WHEN COUNT(i.invoice_id) BETWEEN 2 AND 4 THEN '2. Repeat Buyer (2-4 orders)'
            ELSE '3. Power Buyer (5+ orders)'
        END AS purchase_frequency_bracket
    FROM customers c
    LEFT JOIN invoices i ON c.customer_id = i.customer_id
    GROUP BY c.customer_id
) customer_summary
GROUP BY purchase_frequency_bracket
ORDER BY purchase_frequency_bracket ASC;
