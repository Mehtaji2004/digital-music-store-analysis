-- ==============================================================================
-- DIGITAL MUSIC STORE DATABASE SCHEMA
-- Relational schema optimized for sales analytics and customer behavior modeling
-- Dialect: SQLite / ANSI SQL (Compatible with PostgreSQL and MySQL)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. GENRES
DROP TABLE IF EXISTS playlist_tracks;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS invoice_items;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS genres;

CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL UNIQUE
);

-- 2. ARTISTS
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL
);

-- 3. ALBUMS
CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(160) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER CHECK (release_year >= 1900 AND release_year <= 2030),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id) ON DELETE CASCADE
);

-- 4. TRACKS
CREATE TABLE tracks (
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    album_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    composer VARCHAR(220),
    milliseconds INTEGER NOT NULL CHECK (milliseconds > 0),
    bytes INTEGER CHECK (bytes > 0),
    unit_price NUMERIC(10, 2) NOT NULL DEFAULT 0.99 CHECK (unit_price >= 0),
    FOREIGN KEY (album_id) REFERENCES albums (album_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

-- 5. EMPLOYEES (Sales & Support Staff)
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    reports_to INTEGER,
    birth_date DATE,
    hire_date DATE NOT NULL,
    address VARCHAR(150),
    city VARCHAR(80),
    state VARCHAR(50),
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20),
    phone VARCHAR(30),
    email VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (reports_to) REFERENCES employees (employee_id)
);

-- 6. CUSTOMERS
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    company VARCHAR(100),
    address VARCHAR(150),
    city VARCHAR(80),
    state VARCHAR(50),
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20),
    phone VARCHAR(30),
    email VARCHAR(100) UNIQUE NOT NULL,
    support_rep_id INTEGER,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (support_rep_id) REFERENCES employees (employee_id)
);

-- 7. INVOICES
CREATE TABLE invoices (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    billing_address VARCHAR(150),
    billing_city VARCHAR(80),
    billing_state VARCHAR(50),
    billing_country VARCHAR(50) NOT NULL,
    billing_postal_code VARCHAR(20),
    total NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
);

-- 8. INVOICE ITEMS (Line Items)
CREATE TABLE invoice_items (
    invoice_line_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (invoice_id) REFERENCES invoices (invoice_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks (track_id)
);

-- 9. PLAYLISTS
CREATE TABLE playlists (
    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL
);

-- 10. PLAYLIST TRACKS (Many-to-Many Bridge Table)
CREATE TABLE playlist_tracks (
    playlist_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    PRIMARY KEY (playlist_id, track_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists (playlist_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks (track_id) ON DELETE CASCADE
);

-- ==============================================================================
-- INDEXES FOR QUERY OPTIMIZATION
-- ==============================================================================
CREATE INDEX idx_tracks_album ON tracks (album_id);
CREATE INDEX idx_tracks_genre ON tracks (genre_id);
CREATE INDEX idx_albums_artist ON albums (artist_id);
CREATE INDEX idx_customers_country ON customers (country);
CREATE INDEX idx_customers_support_rep ON customers (support_rep_id);
CREATE INDEX idx_invoices_customer ON invoices (customer_id);
CREATE INDEX idx_invoices_date ON invoices (invoice_date);
CREATE INDEX idx_invoice_items_invoice ON invoice_items (invoice_id);
CREATE INDEX idx_invoice_items_track ON invoice_items (track_id);
