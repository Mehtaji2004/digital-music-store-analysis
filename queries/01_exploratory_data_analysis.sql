-- ==============================================================================
-- 01: EXPLORATORY DATA ANALYSIS (EDA) & FOUNDATIONAL QUERIES
-- Dialect: ANSI SQL / SQLite (Postgres & MySQL compatible)
-- Focus: Aggregations, GROUP BY, Multi-table INNER/LEFT JOINs, Ordering
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Q1: High-Level Catalog Summary
-- Objective: Understand catalog size, pricing bounds, and average track length.
-- Concepts: COUNT(), MIN(), MAX(), AVG(), ROUND()
-- ------------------------------------------------------------------------------
SELECT
    COUNT(track_id) AS total_tracks,
    COUNT(DISTINCT album_id) AS total_albums,
    COUNT(DISTINCT genre_id) AS total_genres,
    ROUND(MIN(unit_price), 2) AS min_price,
    ROUND(MAX(unit_price), 2) AS max_price,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(AVG(milliseconds) / 60000.0, 2) AS avg_track_length_minutes
FROM tracks;


-- ------------------------------------------------------------------------------
-- Q2: Track Catalog Distribution by Genre
-- Objective: Determine which genres dominate the store's inventory.
-- Concepts: INNER JOIN, GROUP BY, ORDER BY, Aggregation
-- ------------------------------------------------------------------------------
SELECT
    g.name AS genre_name,
    COUNT(t.track_id) AS total_tracks,
    ROUND(AVG(t.milliseconds) / 60000.0, 2) AS avg_duration_mins,
    ROUND(AVG(t.unit_price), 2) AS avg_price
FROM genres g
JOIN tracks t ON g.genre_id = t.genre_id
GROUP BY g.genre_id, g.name
ORDER BY total_tracks DESC, g.name ASC;


-- ------------------------------------------------------------------------------
-- Q3: Top 10 Longest Tracks in the Catalog
-- Objective: Identify extended epics / live recordings for audio streaming cache planning.
-- Concepts: Multi-table JOIN (tracks -> albums -> artists), Formatting, LIMIT
-- ------------------------------------------------------------------------------
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
LIMIT 10;


-- ------------------------------------------------------------------------------
-- Q4: Global Customer Geographic Distribution
-- Objective: Find the top customer markets by country and count of unique accounts.
-- Concepts: COUNT(), GROUP BY, HAVING, ORDER BY
-- ------------------------------------------------------------------------------
SELECT
    country,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS customer_share_pct
FROM customers
GROUP BY country
ORDER BY total_customers DESC, country ASC;


-- ------------------------------------------------------------------------------
-- Q5: Albums with Multiple Tracks vs Singletons
-- Objective: Audit artist discography completeness in the catalog.
-- Concepts: JOIN, GROUP BY, HAVING, COUNT()
-- ------------------------------------------------------------------------------
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
ORDER BY track_count DESC, al.release_year ASC;
