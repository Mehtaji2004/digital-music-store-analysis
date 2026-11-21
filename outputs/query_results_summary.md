# Digital Music Store Analysis - Query Results Summary

*Generated automatically from `run_analysis.py` on SQLite database.*

This document contains live executed outputs for all analytical SQL queries in the project.

## Exploratory Data Analysis (EDA) (`queries/01_exploratory_data_analysis.sql`)

### 01: EXPLORATORY DATA ANALYSIS (EDA) & FOUNDATIONAL QUERIES

> **Notes**: ============================================================================== 01: EXPLORATORY DATA ANALYSIS (EDA) & FOUNDATIONAL QUERIES Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible) Focus: Aggregations, GROUP BY, Multi-table INNER/LEFT JOINs, Ordering ============================================================================== Objective: Understand catalog size, pricing bounds, and average track length. Concepts: COUNT(), MIN(), MAX(), AVG(), ROUND()

```sql
SELECT
    COUNT(track_id) AS total_tracks,
    COUNT(DISTINCT album_id) AS total_albums,
    COUNT(DISTINCT genre_id) AS total_genres,
    ROUND(MIN(unit_price), 2) AS min_price,
    ROUND(MAX(unit_price), 2) AS max_price,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(AVG(milliseconds) / 60000.0, 2) AS avg_track_length_minutes
FROM tracks
```

| total_tracks | total_albums | total_genres | min_price | max_price | avg_unit_price | avg_track_length_minutes |
| ------------ | ------------ | ------------ | --------- | --------- | -------------- | ------------------------ |
| 64           | 24           | 10           | 0.99      | 1.29      | 1.14           | 5.14                     |


### Q2: Track Catalog Distribution by Genre

> **Notes**: Objective: Determine which genres dominate the store's inventory. Concepts: INNER JOIN, GROUP BY, ORDER BY, Aggregation

```sql
SELECT
    g.name AS genre_name,
    COUNT(t.track_id) AS total_tracks,
    ROUND(AVG(t.milliseconds) / 60000.0, 2) AS avg_duration_mins,
    ROUND(AVG(t.unit_price), 2) AS avg_price
FROM genres g
JOIN tracks t ON g.genre_id = t.genre_id
GROUP BY g.genre_id, g.name
ORDER BY total_tracks DESC, g.name ASC
```

| genre_name | total_tracks | avg_duration_mins | avg_price |
| ---------- | ------------ | ----------------- | --------- |
| Rock       | 20           | 5.43              | 1.14      |
| Synthwave  | 10           | 3.82              | 1.11      |
| Electronic | 6            | 4.85              | 1.14      |
| Classical  | 5            | 4.62              | 1.17      |
| Hip Hop    | 5            | 4.57              | 1.17      |
| Metal      | 5            | 6.2               | 1.11      |
| Jazz       | 4            | 8.44              | 1.14      |
| Ambient    | 3            | 5.22              | 1.19      |
| Blues      | 3            | 4.92              | 1.19      |
| Indie Folk | 3            | 4.08              | 1.19      |


### Q3: Top 10 Longest Tracks in the Catalog

> **Notes**: Objective: Identify extended epics / live recordings for audio streaming cache planning. Concepts: Multi-table JOIN (tracks -> albums -> artists), Formatting, LIMIT

```sql
SELECT
    t.name AS track_name,
    ar.name AS artist_name,
    al.title AS album_title,
    g.name AS genre,
    ROUND(t.milliseconds / 60000.0, 2) AS duration_minutes,
    ROUND(t.bytes / (1024.0 * 1024.0), 2) AS size_mb
FROM tracks t
JOIN albums al ON t.album_id = al.album_id
JOIN artists ar ON al.artist_id = ar.artist_id
JOIN genres g ON t.genre_id = g.genre_id
ORDER BY t.milliseconds DESC
LIMIT 10
```

| track_name           | artist_name    | album_title        | genre | duration_minutes | size_mb |
| -------------------- | -------------- | ------------------ | ----- | ---------------- | ------- |
| Ascent to Cloudbase  | Cobalt Skies   | Endless Altitude   | Rock  | 12.0             | 22.32   |
| Event Horizon Waltz  | Quantum Groove | Deep Resonance     | Jazz  | 10.17            | 18.88   |
| Subatomic Swing      | Quantum Groove | Deep Resonance     | Jazz  | 9.0              | 16.69   |
| Blue Dimensions      | Quantum Groove | Deep Resonance     | Jazz  | 8.25             | 15.26   |
| Corona Borealis      | Solaris Echo   | Solaris Flare      | Rock  | 8.0              | 14.78   |
| Obsidian Gate        | Apex Pulse     | Pulse Core         | Metal | 8.0              | 14.88   |
| Canyon of Starlight  | Solaris Echo   | Orbital Echoes     | Rock  | 7.5              | 13.92   |
| Highland Vista       | Cobalt Skies   | Azure Horizons     | Rock  | 7.17             | 13.35   |
| Stratosphere Skyline | Cobalt Skies   | Azure Horizons     | Rock  | 6.92             | 12.87   |
| Threshold of Fury    | Apex Pulse     | Overdrive Protocol | Metal | 6.83             | 12.68   |


### Q4: Global Customer Geographic Distribution

> **Notes**: Objective: Find the top customer markets by country and count of unique accounts. Concepts: COUNT(), GROUP BY, HAVING, ORDER BY

```sql
SELECT
    country,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS customer_share_pct
FROM customers
GROUP BY country
ORDER BY total_customers DESC, country ASC
```

| country        | total_customers | customer_share_pct |
| -------------- | --------------- | ------------------ |
| USA            | 10              | 40.0               |
| Brazil         | 4               | 16.0               |
| Canada         | 3               | 12.0               |
| Czech Republic | 2               | 8.0                |
| Austria        | 1               | 4.0                |
| Belgium        | 1               | 4.0                |
| Denmark        | 1               | 4.0                |
| Germany        | 1               | 4.0                |
| Norway         | 1               | 4.0                |
| Portugal       | 1               | 4.0                |


### Q5: Albums with Multiple Tracks vs Singletons

> **Notes**: Objective: Audit artist discography completeness in the catalog. Concepts: JOIN, GROUP BY, HAVING, COUNT()

```sql
SELECT
    ar.name AS artist_name,
    al.title AS album_title,
    al.release_year,
    COUNT(t.track_id) AS track_count
FROM albums al
JOIN artists ar ON al.artist_id = ar.artist_id
JOIN tracks t ON al.album_id = t.album_id
GROUP BY al.album_id, ar.name, al.title, al.release_year
HAVING COUNT(t.track_id) >= 3
ORDER BY track_count DESC, al.release_year ASC
```

| artist_name           | album_title             | release_year | track_count |
| --------------------- | ----------------------- | ------------ | ----------- |
| Quantum Groove        | Deep Resonance          | 2019         | 4           |
| Echo Chamber          | Whispering Shadows      | 2020         | 4           |
| Starlight Symphony    | Celestial Harmony       | 2021         | 4           |
| Solaris Echo          | Orbital Echoes          | 2018         | 3           |
| Cobalt Skies          | Azure Horizons          | 2018         | 3           |
| Velvet Reverie        | Silk and Strings        | 2019         | 3           |
| Terra Nova Collective | Earth and Sky           | 2019         | 3           |
| Neon Horizon          | Synthesized Reflections | 2020         | 3           |
| Apex Pulse            | Pulse Core              | 2020         | 3           |
| Luna Collective       | Moonlight Serenade      | 2020         | 3           |
| Aurora Drift          | Electric Dawn           | 2021         | 3           |
| The Midnight Velocity | Subatomic Grooves       | 2021         | 3           |
| Horizon Beat          | Sunset Boulevard        | 2021         | 3           |
| Prism Wave            | Spectrum Odyssey        | 2022         | 3           |
| The Midnight Velocity | Velocity Unbound        | 2023         | 3           |


## Sales & Revenue Business Intelligence (`queries/02_sales_and_revenue_metrics.sql`)

### Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)

> **Notes**: ============================================================================== 02: SALES & REVENUE METRICS (BUSINESS INTELLIGENCE) Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible) Focus: Multi-table relational joins, Revenue aggregation, Subqueries, CASE ============================================================================== Objective: Rank musical artists by actual cash revenue generated from track sales. Concepts: Multi-table JOIN (artists -> albums -> tracks -> invoice_items), SUM()

```sql
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
LIMIT 10
```

| artist_id | artist_name           | tracks_sold | total_revenue | revenue_share_pct |
| --------- | --------------------- | ----------- | ------------- | ----------------- |
| 9         | Starlight Symphony    | 26          | 28.74         | 10.39             |
| 7         | Velvet Reverie        | 22          | 26.88         | 9.72              |
| 4         | The Midnight Velocity | 20          | 24.0          | 8.68              |
| 11        | Cobalt Skies          | 19          | 23.31         | 8.43              |
| 6         | Echo Chamber          | 21          | 22.29         | 8.06              |
| 5         | Solaris Echo          | 20          | 22.2          | 8.03              |
| 8         | Apex Pulse            | 18          | 19.92         | 7.2               |
| 2         | Neon Horizon          | 18          | 19.02         | 6.88              |
| 12        | Luna Collective       | 14          | 16.86         | 6.1               |
| 1         | Aurora Drift          | 14          | 15.66         | 5.66              |


### Q2: Geographic Market Performance (Revenue, Orders, and AOV)

> **Notes**: Objective: Evaluate revenue and Average Order Value (AOV) across countries. Concepts: GROUP BY, COUNT(DISTINCT), SUM(), AVG(), Derived Metrics

```sql
SELECT
    billing_country,
    COUNT(DISTINCT invoice_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total), 2) AS total_sales,
    ROUND(AVG(total), 2) AS average_order_value,
    ROUND(SUM(total) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM invoices
GROUP BY billing_country
ORDER BY total_sales DESC
```

| billing_country | total_orders | unique_customers | total_sales | average_order_value | revenue_per_customer |
| --------------- | ------------ | ---------------- | ----------- | ------------------- | -------------------- |
| USA             | 38           | 9                | 116.46      | 3.06                | 12.94                |
| Brazil          | 22           | 4                | 79.02       | 3.59                | 19.75                |
| Czech Republic  | 8            | 2                | 31.53       | 3.94                | 15.77                |
| Canada          | 11           | 3                | 29.94       | 2.72                | 9.98                 |
| Belgium         | 2            | 1                | 8.13        | 4.07                | 8.13                 |
| Norway          | 2            | 1                | 5.25        | 2.63                | 5.25                 |
| Germany         | 1            | 1                | 3.57        | 3.57                | 3.57                 |
| Austria         | 1            | 1                | 2.58        | 2.58                | 2.58                 |


### Q3: Sales Support Agent Performance Leaderboard

> **Notes**: Objective: Compare support representatives on assigned customer revenue, portfolio size, and conversion health. Concepts: LEFT JOIN (employees -> customers -> invoices), Self-joins/hierarchies

```sql
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
ORDER BY total_revenue_generated DESC
```

| employee_id | sales_rep     | title               | hire_date  | assigned_customers | total_invoices_closed | total_revenue_generated | revenue_per_assigned_customer |
| ----------- | ------------- | ------------------- | ---------- | ------------------ | --------------------- | ----------------------- | ----------------------------- |
| 3           | Jane Peacock  | Sales Support Agent | 2020-04-01 | 8                  | 37                    | 121.74                  | 15.22                         |
| 5           | Steve Johnson | Sales Support Agent | 2021-10-17 | 7                  | 25                    | 82.68                   | 11.81                         |
| 4           | Margaret Park | Sales Support Agent | 2021-01-15 | 10                 | 23                    | 72.06                   | 7.21                          |
| 2           | Nancy Edwards | Sales Manager       | 2019-05-01 | 0                  | 0                     | 0.0                     | NULL                          |


### Q4: Most Popular Genre in Each Country

> **Notes**: Objective: Identify customer taste variations by country to inform localized promotions. Concepts: CTE (Common Table Expression), Nested Aggregations, GROUP BY

```sql
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
ORDER BY cgs.units_purchased DESC, cgs.country ASC
```

| country        | top_genre  | units_purchased | genre_revenue |
| -------------- | ---------- | --------------- | ------------- |
| USA            | Rock       | 34              | 37.26         |
| Brazil         | Rock       | 19              | 22.11         |
| Canada         | Rock       | 8               | 9.42          |
| Czech Republic | Synthwave  | 8               | 8.82          |
| Belgium        | Classical  | 2               | 2.58          |
| Belgium        | Rock       | 2               | 1.98          |
| Germany        | Rock       | 2               | 2.28          |
| Norway         | Rock       | 2               | 2.28          |
| Austria        | Blues      | 1               | 1.29          |
| Austria        | Electronic | 1               | 1.29          |


### Q5: Customer Cohort Purchase Frequency (Repeat vs One-Time Buyers)

> **Notes**: Objective: Measure customer retention rate and repeat purchase behavior. Concepts: Subqueries, CASE WHEN, Conditional Aggregation

```sql
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
ORDER BY purchase_frequency_bracket ASC
```

| purchase_frequency_bracket   | customer_count | pct_of_customer_base | total_spend_bracket | avg_spend_per_customer |
| ---------------------------- | -------------- | -------------------- | ------------------- | ---------------------- |
| 1. One-Time Buyer            | 5              | 20.0                 | 13.68               | 2.74                   |
| 2. Repeat Buyer (2-4 orders) | 11             | 44.0                 | 118.26              | 10.75                  |
| 3. Power Buyer (5+ orders)   | 9              | 36.0                 | 144.54              | 24.09                  |


## Advanced Analytics & Window Functions (`queries/03_advanced_analytics.sql`)

### Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)

> **Notes**: ============================================================================== 03: ADVANCED ANALYTICS (WINDOW FUNCTIONS, CTES & TIME SERIES) Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible) Focus: RANK(), DENSE_RANK(), ROW_NUMBER(), LEAD(), LAG(), SUM() OVER(), NTILE() ============================================================================== Objective: Track financial traction by charting monthly revenue alongside a running total. Concepts: DATE formatting, CTEs, Window Function: SUM() OVER (ORDER BY ...)

```sql
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
ORDER BY sales_month ASC
```

| sales_month | order_count | monthly_revenue | cumulative_revenue | rolling_3mo_avg_revenue |
| ----------- | ----------- | --------------- | ------------------ | ----------------------- |
| 2024-01     | 1           | 4.56            | 4.56               | 4.56                    |
| 2024-02     | 3           | 9.12            | 13.68              | 6.84                    |
| 2024-03     | 1           | 2.58            | 16.26              | 5.42                    |
| 2024-04     | 4           | 9.12            | 25.38              | 6.94                    |
| 2024-05     | 1           | 1.98            | 27.36              | 4.56                    |
| 2024-06     | 3           | 11.7            | 39.06              | 7.6                     |
| 2024-08     | 3           | 10.8            | 49.86              | 8.16                    |
| 2024-09     | 4           | 17.64           | 67.5               | 13.38                   |
| 2024-10     | 3           | 6.84            | 74.34              | 11.76                   |
| 2024-12     | 1           | 0.99            | 75.33              | 8.49                    |
| 2025-01     | 3           | 9.42            | 84.75              | 5.75                    |
| 2025-02     | 2           | 4.86            | 89.61              | 5.09                    |
| 2025-03     | 1           | 4.56            | 94.17              | 6.28                    |
| 2025-04     | 4           | 10.8            | 104.97             | 6.74                    |
| 2025-05     | 2           | 11.01           | 115.98             | 8.79                    |
| 2025-06     | 1           | 0.99            | 116.97             | 7.6                     |
| 2025-07     | 2           | 9.72            | 126.69             | 7.24                    |
| 2025-08     | 2           | 4.56            | 131.25             | 5.09                    |
| 2025-09     | 2           | 3.27            | 134.52             | 5.85                    |
| 2025-10     | 5           | 24.39           | 158.91             | 10.74                   |

*Showing top 20 of 31 rows.*

### Q2: Month-over-Month (MoM) Revenue Growth Rate

> **Notes**: Objective: Determine momentum and revenue volatility across consecutive months. Concepts: LAG(), Window Functions, Percentage calculation, CASE WHEN (division by zero)

```sql
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
ORDER BY sales_month ASC
```

| sales_month | monthly_revenue | previous_month_revenue | mom_dollar_change | mom_growth_pct |
| ----------- | --------------- | ---------------------- | ----------------- | -------------- |
| 2024-01     | 4.56            | 0.0                    | 4.56              | 0.0            |
| 2024-02     | 9.12            | 4.56                   | 4.56              | 100.0          |
| 2024-03     | 2.58            | 9.12                   | -6.54             | -71.71         |
| 2024-04     | 9.12            | 2.58                   | 6.54              | 253.49         |
| 2024-05     | 1.98            | 9.12                   | -7.14             | -78.29         |
| 2024-06     | 11.7            | 1.98                   | 9.72              | 490.91         |
| 2024-08     | 10.8            | 11.7                   | -0.9              | -7.69          |
| 2024-09     | 17.64           | 10.8                   | 6.84              | 63.33          |
| 2024-10     | 6.84            | 17.64                  | -10.8             | -61.22         |
| 2024-12     | 0.99            | 6.84                   | -5.85             | -85.53         |
| 2025-01     | 9.42            | 0.99                   | 8.43              | 851.52         |
| 2025-02     | 4.86            | 9.42                   | -4.56             | -48.41         |
| 2025-03     | 4.56            | 4.86                   | -0.3              | -6.17          |
| 2025-04     | 10.8            | 4.56                   | 6.24              | 136.84         |
| 2025-05     | 11.01           | 10.8                   | 0.21              | 1.94           |
| 2025-06     | 0.99            | 11.01                  | -10.02            | -91.01         |
| 2025-07     | 9.72            | 0.99                   | 8.73              | 881.82         |
| 2025-08     | 4.56            | 9.72                   | -5.16             | -53.09         |
| 2025-09     | 3.27            | 4.56                   | -1.29             | -28.29         |
| 2025-10     | 24.39           | 3.27                   | 21.12             | 645.87         |

*Showing top 20 of 31 rows.*

### Q3: Top 2 Best-Selling Tracks per Genre (Partitioned Ranking)

> **Notes**: Objective: Curate genre-specific landing pages and highlight top performers. Concepts: DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...), Multi-table CTE

```sql
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
ORDER BY genre_name ASC, genre_rank ASC, track_revenue DESC
```

| genre_name | genre_rank | track_name           | artist_name           | units_sold | track_revenue |
| ---------- | ---------- | -------------------- | --------------------- | ---------- | ------------- |
| Ambient    | 1          | Aurora Cascade       | Prism Wave            | 6          | 7.74          |
| Ambient    | 2          | Ethereal Tide        | Prism Wave            | 4          | 3.96          |
| Blues      | 1          | Backporch Shuffle    | Horizon Beat          | 6          | 5.94          |
| Blues      | 2          | Late Night Barstool  | Horizon Beat          | 5          | 6.45          |
| Classical  | 1          | Cello Rhapsody       | Velvet Reverie        | 8          | 10.32         |
| Classical  | 2          | Nocturne No. 5       | Velvet Reverie        | 5          | 6.45          |
| Electronic | 1          | Hyperdrive Tempo     | The Midnight Velocity | 7          | 9.03          |
| Electronic | 2          | Kinetic Pulse        | The Midnight Velocity | 4          | 5.16          |
| Hip Hop    | 1          | Urban Rhythm Section | Terra Nova Collective | 4          | 5.16          |
| Hip Hop    | 2          | Midnight Asphalt     | Terra Nova Collective | 3          | 2.97          |
| Hip Hop    | 2          | Concrete Canvas      | Terra Nova Collective | 3          | 2.97          |
| Indie Folk | 1          | Autumn Cabin Songs   | Luna Collective       | 7          | 9.03          |
| Indie Folk | 2          | Mountain River Run   | Luna Collective       | 4          | 3.96          |
| Jazz       | 1          | Blue Dimensions      | Quantum Groove        | 4          | 3.96          |
| Jazz       | 2          | Subatomic Swing      | Quantum Groove        | 3          | 3.87          |
| Jazz       | 2          | Event Horizon Waltz  | Quantum Groove        | 3          | 3.87          |
| Metal      | 1          | Obsidian Gate        | Apex Pulse            | 4          | 5.16          |
| Metal      | 2          | Iron Catalyst        | Apex Pulse            | 4          | 3.96          |
| Metal      | 2          | Molten Core Run      | Apex Pulse            | 4          | 3.96          |
| Rock       | 1          | Ridge Line Wind      | Cobalt Skies          | 6          | 7.74          |

*Showing top 20 of 25 rows.*

### Q4: Customer Lifetime Value (LTV) Quartile Distribution

> **Notes**: Objective: Segment the customer base into 4 spend tiers (VIP, Tier 2, Tier 3, Low). Concepts: NTILE(4) Window Function, Subqueries, Segment Aggregation

```sql
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
ORDER BY ltv_quartile ASC
```

| customer_tier                        | customer_count | min_spend_in_tier | max_spend_in_tier | avg_spend_in_tier | tier_total_revenue | pct_of_store_revenue |
| ------------------------------------ | -------------- | ----------------- | ----------------- | ----------------- | ------------------ | -------------------- |
| Tier 1 - VIP High Spenders (Top 25%) | 6              | 18.93             | 33.12             | 24.54             | 147.21             | 53.2                 |
| Tier 2 - Above Average Spenders      | 6              | 9.51              | 16.26             | 13.83             | 82.98              | 30.0                 |
| Tier 3 - Moderate Spenders           | 5              | 4.56              | 8.13              | 6.52              | 32.61              | 11.8                 |
| Tier 4 - Entry-Level Spenders        | 5              | 0.99              | 3.57              | 2.74              | 13.68              | 4.9                  |


### Q5: Days Since Last Purchase & Churn Risk Analysis

> **Notes**: Objective: Identify inactive customers who have lapsed beyond 180 days since their last order. Concepts: JULIANDAY(), MAX() Date aggregation, CASE WHEN, Filtering

```sql
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
ORDER BY days_since_last_purchase DESC
```

| customer_id | customer_name         | country        | last_purchase_date  | days_since_last_purchase | order_count | total_spend | retention_status       |
| ----------- | --------------------- | -------------- | ------------------- | ------------------------ | ----------- | ----------- | ---------------------- |
| 7           | Astrid Gruber         | Austria        | 2024-04-28 18:47:00 | 936.0                    | 1           | 2.58        | Churn Risk (>180 days) |
| 2           | Leonie Kohler         | Germany        | 2024-06-05 11:47:00 | 899.0                    | 1           | 3.57        | Churn Risk (>180 days) |
| 24          | Richard Cunningham    | USA            | 2024-09-09 21:06:00 | 802.0                    | 1           | 2.97        | Churn Risk (>180 days) |
| 15          | Jennifer Peterson     | Canada         | 2025-02-12 14:38:00 | 646.0                    | 1           | 0.99        | Churn Risk (>180 days) |
| 23          | John Gordon           | USA            | 2025-08-28 11:45:00 | 450.0                    | 3           | 7.83        | Churn Risk (>180 days) |
| 4           | Bjorn Hansen          | Norway         | 2026-01-02 22:43:00 | 322.0                    | 2           | 5.25        | Churn Risk (>180 days) |
| 12          | Roberto Almeida       | Brazil         | 2026-01-17 18:44:00 | 307.0                    | 4           | 18.93       | Churn Risk (>180 days) |
| 20          | Dan Miller            | USA            | 2026-01-19 13:13:00 | 305.0                    | 1           | 3.57        | Churn Risk (>180 days) |
| 6           | Helena Holy           | Czech Republic | 2026-02-26 08:55:00 | 268.0                    | 3           | 15.27       | Churn Risk (>180 days) |
| 8           | Daan Peeters          | Belgium        | 2026-04-20 08:46:00 | 215.0                    | 2           | 8.13        | Churn Risk (>180 days) |
| 1           | Luis Goncalves        | Brazil         | 2026-07-08 22:41:00 | 135.0                    | 10          | 33.12       | Warm (61-180 days)     |
| 13          | Fernanda Ramos        | Brazil         | 2026-07-09 21:23:00 | 134.0                    | 4           | 12.99       | Warm (61-180 days)     |
| 16          | Frank Harris          | USA            | 2026-07-09 16:48:00 | 134.0                    | 7           | 19.23       | Warm (61-180 days)     |
| 22          | Heather Leacock       | USA            | 2026-07-22 17:25:00 | 121.0                    | 8           | 22.89       | Warm (61-180 days)     |
| 3           | Francois Tremblay     | Canada         | 2026-08-06 09:55:00 | 107.0                    | 7           | 22.11       | Warm (61-180 days)     |
| 11          | Alexandre Rocha       | Brazil         | 2026-08-07 17:56:00 | 105.0                    | 4           | 13.98       | Warm (61-180 days)     |
| 19          | Tim Goyer             | USA            | 2026-09-06 08:43:00 | 76.0                     | 2           | 4.56        | Warm (61-180 days)     |
| 21          | Kathy Chase           | USA            | 2026-09-17 20:59:00 | 64.0                     | 3           | 9.51        | Warm (61-180 days)     |
| 5           | Frantisek Wichterlova | Czech Republic | 2026-09-21 20:21:00 | 60.0                     | 5           | 16.26       | Active (0-60 days)     |
| 18          | Michelle Brooks       | USA            | 2026-10-05 16:55:00 | 46.0                     | 3           | 14.97       | Active (0-60 days)     |

*Showing top 20 of 25 rows.*

## RFM Customer Segmentation & Strategy (`queries/04_rfm_customer_segmentation.sql`)

### Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)

> **Notes**: ============================================================================== 04: RFM CUSTOMER SEGMENTATION & LIFETIME VALUE MODEL Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible) Focus: Multi-stage CTEs, NTILE() scoring, Business rule segmentation ============================================================================== Objective: Score customers across three critical behavioral dimensions: - Recency (R): How recently did the customer purchase? (Lower days = Higher score) - Frequency (F): How often do they purchase? - Monetary (M): How much money do they spend? Then map them into actionable customer lifecycle segments with strategic recommendations. Recency: fewer days ago = higher rank (4 is best, 1 is worst) Frequency: more orders = higher rank Monetary: more total spend = higher rank

```sql
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
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
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
ORDER BY composite_rfm_score DESC, monetary DESC
```

| customer_id | customer_name         | country        | recency_days | total_orders | total_spent_usd | r_score | f_score | m_score | composite_rfm_score | rfm_segment                      |
| ----------- | --------------------- | -------------- | ------------ | ------------ | --------------- | ------- | ------- | ------- | ------------------- | -------------------------------- |
| 17          | Jack Smith            | USA            | 27.0         | 10           | 30.93           | 4       | 4       | 4       | 12                  | 1. Champions                     |
| 1           | Luis Goncalves        | Brazil         | 135.0        | 10           | 33.12           | 3       | 4       | 4       | 11                  | 1. Champions                     |
| 22          | Heather Leacock       | USA            | 121.0        | 8            | 22.89           | 3       | 4       | 4       | 11                  | 1. Champions                     |
| 3           | Francois Tremblay     | Canada         | 107.0        | 7            | 22.11           | 3       | 4       | 4       | 11                  | 1. Champions                     |
| 16          | Frank Harris          | USA            | 134.0        | 7            | 19.23           | 3       | 4       | 4       | 11                  | 1. Champions                     |
| 5           | Frantisek Wichterlova | Czech Republic | 60.0         | 5            | 16.26           | 4       | 4       | 3       | 11                  | 1. Champions                     |
| 18          | Michelle Brooks       | USA            | 46.0         | 3            | 14.97           | 4       | 3       | 3       | 10                  | 1. Champions                     |
| 21          | Kathy Chase           | USA            | 64.0         | 3            | 9.51            | 4       | 3       | 3       | 10                  | 1. Champions                     |
| 12          | Roberto Almeida       | Brazil         | 307.0        | 4            | 18.93           | 2       | 3       | 4       | 9                   | 4. At Risk (High Value Inactive) |
| 11          | Alexandre Rocha       | Brazil         | 105.0        | 4            | 13.98           | 3       | 3       | 3       | 9                   | 1. Champions                     |
| 13          | Fernanda Ramos        | Brazil         | 134.0        | 4            | 12.99           | 3       | 3       | 3       | 9                   | 1. Champions                     |
| 6           | Helena Holy           | Czech Republic | 268.0        | 3            | 15.27           | 2       | 3       | 3       | 8                   | 4. At Risk (High Value Inactive) |
| 14          | Mark Philips          | Canada         | 33.0         | 3            | 6.84            | 4       | 2       | 2       | 8                   | 2. Loyal Customers               |
| 19          | Tim Goyer             | USA            | 76.0         | 2            | 4.56            | 4       | 2       | 2       | 8                   | 2. Loyal Customers               |
| 8           | Daan Peeters          | Belgium        | 215.0        | 2            | 8.13            | 2       | 2       | 2       | 6                   | 5. Needs Attention               |
| 23          | John Gordon           | USA            | 450.0        | 3            | 7.83            | 2       | 2       | 2       | 6                   | 5. Needs Attention               |
| 4           | Bjorn Hansen          | Norway         | 322.0        | 2            | 5.25            | 2       | 2       | 2       | 6                   | 5. Needs Attention               |
| 20          | Dan Miller            | USA            | 305.0        | 1            | 3.57            | 2       | 2       | 2       | 6                   | 5. Needs Attention               |
| 2           | Leonie Kohler         | Germany        | 899.0        | 1            | 3.57            | 1       | 1       | 1       | 3                   | 6. Hibernating / Lost            |
| 24          | Richard Cunningham    | USA            | 802.0        | 1            | 2.97            | 1       | 1       | 1       | 3                   | 6. Hibernating / Lost            |

*Showing top 20 of 25 rows.*

### Q2: Executive RFM Segment Summary & Strategic Playbook

> **Notes**: Objective: Provide executive leadership with total revenue, customer count, and marketing action items per RFM cohort.

```sql
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
ORDER BY total_segment_revenue DESC
```

| rfm_segment                      | customer_count | pct_of_customers | total_segment_revenue | avg_customer_value | marketing_action_strategy                                                                        |
| -------------------------------- | -------------- | ---------------- | --------------------- | ------------------ | ------------------------------------------------------------------------------------------------ |
| 1. Champions                     | 10             | 40.0             | 195.99                | 19.6               | Reward with VIP early track releases, exclusive vinyl discounts, and referral perks              |
| 4. At Risk (High Value Inactive) | 2              | 8.0              | 34.2                  | 17.1               | Re-engagement email campaign with personalized win-back voucher ($5 off)                         |
| 5. Needs Attention               | 4              | 16.0             | 24.78                 | 6.2                | Time-sensitive flash sales and recommendations based on past genres                              |
| 2. Loyal Customers               | 2              | 8.0              | 11.4                  | 5.7                | Upsell personalized multi-genre bundles and subscription memberships                             |
| 6. Hibernating / Lost            | 7              | 28.0             | 10.11                 | 1.44               | Re-activate via automated email drip and win-back voucher, or archive if inactive over 12 months |

