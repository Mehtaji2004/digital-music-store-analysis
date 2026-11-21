-- ==============================================================================
-- 04: RFM CUSTOMER SEGMENTATION & LIFETIME VALUE MODEL
-- Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)
-- Focus: Multi-stage CTEs, NTILE() scoring, Business rule segmentation
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Q1: Full RFM (Recency, Frequency, Monetary) Customer Scoring & Action Plan
-- Objective: Score customers across three critical behavioral dimensions:
--   - Recency (R): How recently did the customer purchase? (Lower days = Higher score)
--   - Frequency (F): How often do they purchase?
--   - Monetary (M): How much money do they spend?
-- Then map them into actionable customer lifecycle segments with strategic recommendations.
-- ------------------------------------------------------------------------------
WITH CustomerBaseMetrics AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.country,
        c.email,
        COUNT(i.invoice_id) AS frequency,
        ROUND(COALESCE(SUM(i.total), 0.0), 2) AS monetary,
        ROUND(COALESCE(JULIANDAY('2026-11-21') - JULIANDAY(MAX(i.invoice_date)), 999), 0) AS recency_days
    FROM customers c
    LEFT JOIN invoices i ON c.customer_id = i.customer_id
    GROUP BY c.customer_id, customer_name, c.country, c.email
),
RFMScores AS (
    SELECT
        customer_id,
        customer_name,
        country,
        email,
        recency_days,
        frequency,
        monetary,
        -- Recency: fewer days ago = higher rank (4 is best, 1 is worst)
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Frequency: more orders = higher rank
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        -- Monetary: more total spend = higher rank
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM CustomerBaseMetrics
),
SegmentedCustomers AS (
    SELECT
        customer_id,
        customer_name,
        country,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        (r_score + f_score + m_score) AS composite_rfm_score,
        CASE
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN '1. Champions'
            WHEN r_score >= 3 AND f_score >= 2 THEN '2. Loyal Customers'
            WHEN r_score >= 3 AND f_score = 1 THEN '3. Recent / New Customers'
            WHEN r_score <= 2 AND f_score >= 3 THEN '4. At Risk (High Value Inactive)'
            WHEN r_score <= 2 AND f_score = 2 THEN '5. Needs Attention'
            ELSE '6. Hibernating / Lost'
        END AS rfm_segment
    FROM RFMScores
)
SELECT
    customer_id,
    customer_name,
    country,
    recency_days,
    frequency AS total_orders,
    monetary AS total_spent_usd,
    r_score,
    f_score,
    m_score,
    composite_rfm_score,
    rfm_segment
FROM SegmentedCustomers
ORDER BY composite_rfm_score DESC, monetary DESC;


-- ------------------------------------------------------------------------------
-- Q2: Executive RFM Segment Summary & Strategic Playbook
-- Objective: Provide executive leadership with total revenue, customer count,
--            and marketing action items per RFM cohort.
-- ------------------------------------------------------------------------------
WITH CustomerBaseMetrics AS (
    SELECT
        c.customer_id,
        COUNT(i.invoice_id) AS frequency,
        ROUND(COALESCE(SUM(i.total), 0.0), 2) AS monetary,
        ROUND(COALESCE(JULIANDAY('2026-11-21') - JULIANDAY(MAX(i.invoice_date)), 999), 0) AS recency_days
    FROM customers c
    LEFT JOIN invoices i ON c.customer_id = i.customer_id
    GROUP BY c.customer_id
),
RFMScores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM CustomerBaseMetrics
),
SegmentedCustomers AS (
    SELECT
        customer_id,
        monetary,
        CASE
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN '1. Champions'
            WHEN r_score >= 3 AND f_score >= 2 THEN '2. Loyal Customers'
            WHEN r_score >= 3 AND f_score = 1 THEN '3. Recent / New Customers'
            WHEN r_score <= 2 AND f_score >= 3 THEN '4. At Risk (High Value Inactive)'
            WHEN r_score <= 2 AND f_score = 2 THEN '5. Needs Attention'
            ELSE '6. Hibernating / Lost'
        END AS rfm_segment
    FROM RFMScores
)
SELECT
    rfm_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS pct_of_customers,
    ROUND(SUM(monetary), 2) AS total_segment_revenue,
    ROUND(AVG(monetary), 2) AS avg_customer_value,
    CASE rfm_segment
        WHEN '1. Champions' THEN 'Reward with VIP early track releases, exclusive vinyl discounts, and referral perks'
        WHEN '2. Loyal Customers' THEN 'Upsell personalized multi-genre bundles and subscription memberships'
        WHEN '3. Recent / New Customers' THEN 'Onboard with welcome discount series and genre onboarding quiz'
        WHEN '4. At Risk (High Value Inactive)' THEN 'Re-engagement email campaign with personalized win-back voucher ($5 off)'
        WHEN '5. Needs Attention' THEN 'Time-sensitive flash sales and recommendations based on past genres'
        ELSE 'Re-activate via automated email drip and win-back voucher, or archive if inactive over 12 months'
    END AS marketing_action_strategy
FROM SegmentedCustomers
GROUP BY rfm_segment
ORDER BY total_segment_revenue DESC;
