"""
Seed data generator for Digital Music Store Database
Generates realistic, normalized data across fictional artists, albums, tracks,
employees, customers, invoices, and invoice line items with mathematical integrity.
All entity names and music metadata are 100% original and fictional.
"""

import os
import random
from datetime import datetime, timedelta

random.seed(42)

def generate_seed_sql():
    sql = []
    sql.append("-- ==============================================================================")
    sql.append("-- DIGITAL MUSIC STORE SAMPLE DATASET (SYNTHETIC / ORIGINAL DATA)")
    sql.append("-- Generated for SQL learning, data analysis, and portfolio demonstration")
    sql.append("-- ==============================================================================\n")

    # 1. GENRES
    genres = [
        (1, 'Rock'),
        (2, 'Jazz'),
        (3, 'Metal'),
        (4, 'Electronic'),
        (5, 'Synthwave'),
        (6, 'Hip Hop'),
        (7, 'Classical'),
        (8, 'Blues'),
        (9, 'Indie Folk'),
        (10, 'Ambient')
    ]
    sql.append("-- 1. GENRES")
    for gid, name in genres:
        sql.append(f"INSERT INTO genres (genre_id, name) VALUES ({gid}, '{name}');")
    sql.append("")

    # 2. ARTISTS (Original / Fictional)
    artists = [
        (1, 'Aurora Drift'),
        (2, 'Neon Horizon'),
        (3, 'Quantum Groove'),
        (4, 'The Midnight Velocity'),
        (5, 'Solaris Echo'),
        (6, 'Echo Chamber'),
        (7, 'Velvet Reverie'),
        (8, 'Apex Pulse'),
        (9, 'Starlight Symphony'),
        (10, 'Terra Nova Collective'),
        (11, 'Cobalt Skies'),
        (12, 'Luna Collective'),
        (13, 'Horizon Beat'),
        (14, 'Prism Wave')
    ]
    sql.append("-- 2. ARTISTS")
    for aid, name in artists:
        escaped_name = name.replace("'", "''")
        sql.append(f"INSERT INTO artists (artist_id, name) VALUES ({aid}, '{escaped_name}');")
    sql.append("")

    # 3. ALBUMS (Original / Fictional)
    albums = [
        (1, 'Electric Dawn', 1, 2021),
        (2, 'Midnight Express', 1, 2023),
        (3, 'Synthesized Reflections', 2, 2020),
        (4, 'Retrograde Nights', 2, 2022),
        (5, 'Deep Resonance', 3, 2019),
        (6, 'Subatomic Grooves', 4, 2021),
        (7, 'Velocity Unbound', 4, 2023),
        (8, 'Orbital Echoes', 5, 2018),
        (9, 'Solaris Flare', 5, 2022),
        (10, 'Whispering Shadows', 6, 2020),
        (11, 'Sonic Reverberation', 6, 2023),
        (12, 'Silk and Strings', 7, 2019),
        (13, 'Nocturne Tales', 7, 2022),
        (14, 'Pulse Core', 8, 2020),
        (15, 'Overdrive Protocol', 8, 2022),
        (16, 'Celestial Harmony', 9, 2021),
        (17, 'Astral Wanderer', 9, 2023),
        (18, 'Earth and Sky', 10, 2019),
        (19, 'Roots and Rhythm', 10, 2022),
        (20, 'Azure Horizons', 11, 2018),
        (21, 'Endless Altitude', 11, 2021),
        (22, 'Moonlight Serenade', 12, 2020),
        (23, 'Sunset Boulevard', 13, 2021),
        (24, 'Spectrum Odyssey', 14, 2022)
    ]
    sql.append("-- 3. ALBUMS")
    for alb_id, title, aid, yr in albums:
        sql.append(f"INSERT INTO albums (album_id, title, artist_id, release_year) VALUES ({alb_id}, '{title}', {aid}, {yr});")
    sql.append("")

    # 4. TRACKS (Original / Fictional)
    tracks_data = [
        # Aurora Drift - Electric Dawn (Rock - 1)
        ('Starlight Anthem', 1, 1, 'Marcus Chen', 315000, 10200000, 1.29),
        ('Electric Mirage', 1, 1, 'Marcus Chen', 242000, 7800000, 0.99),
        ('Northern Aurora', 1, 1, 'Marcus Chen, Sofia Alvarez', 285000, 9200000, 1.29),
        # Aurora Drift - Midnight Express
        ('Midnight Freeway', 2, 1, 'Marcus Chen', 215000, 7000000, 0.99),
        ('Neon Horizon Rush', 2, 1, 'Sofia Alvarez', 230000, 7400000, 0.99),
        # Neon Horizon - Synthesized Reflections (Synthwave - 5)
        ('Cybernetic Sunset', 3, 5, 'Julian Drake', 260000, 8400000, 1.29),
        ('Grid Runner', 3, 5, 'Julian Drake', 210000, 6800000, 0.99),
        ('Analog Heartbeat', 3, 5, 'Julian Drake', 245000, 7900000, 0.99),
        # Neon Horizon - Retrograde Nights
        ('Future Memory', 4, 5, 'Julian Drake', 255000, 8200000, 0.99),
        # Quantum Groove - Deep Resonance (Jazz - 2)
        ('Subatomic Swing', 5, 2, 'Elena Rostova', 540000, 17500000, 1.29),
        ('Blue Dimensions', 5, 2, 'Elena Rostova', 495000, 16000000, 0.99),
        ('Midnight Modal', 5, 2, 'Elena Rostova, Liam Thorne', 380000, 12300000, 0.99),
        ('Event Horizon Waltz', 5, 2, 'Elena Rostova', 610000, 19800000, 1.29),
        # The Midnight Velocity - Subatomic Grooves (Electronic - 4)
        ('Kinetic Pulse', 6, 4, 'Liam Thorne', 310000, 10000000, 1.29),
        ('Modular Cascade', 6, 4, 'Liam Thorne', 225000, 7300000, 0.99),
        ('Bass Frequency One', 6, 4, 'Liam Thorne', 280000, 9100000, 1.29),
        # The Midnight Velocity - Velocity Unbound
        ('Hyperdrive Tempo', 7, 4, 'Liam Thorne, Maya Lin', 345000, 11200000, 1.29),
        ('Sonic Waveform', 7, 4, 'Liam Thorne', 270000, 8700000, 0.99),
        ('Zero Gravity Groove', 7, 4, 'Liam Thorne, Maya Lin', 315000, 10200000, 0.99),
        # Solaris Echo - Orbital Echoes (Rock - 1)
        ('Solar Flare Ignition', 8, 1, 'Alex Vance', 290000, 9400000, 0.99),
        ('Canyon of Starlight', 8, 1, 'Alex Vance, Chloe Bennett', 450000, 14600000, 1.29),
        ('Winds of Neptune', 8, 1, 'Alex Vance', 260000, 8400000, 0.99),
        # Solaris Echo - Solaris Flare
        ('Corona Borealis', 9, 1, 'Alex Vance', 480000, 15500000, 1.29),
        # Echo Chamber - Whispering Shadows (Rock - 1)
        ('Shadows in the Rain', 10, 1, 'David Sterling', 295000, 9600000, 1.29),
        ('Cobalt Echoes', 10, 1, 'David Sterling', 240000, 7800000, 0.99),
        ('Underground River', 10, 1, 'David Sterling', 215000, 7000000, 0.99),
        ('Static and Distortion', 10, 1, 'David Sterling', 250000, 8100000, 0.99),
        # Echo Chamber - Sonic Reverberation
        ('Chamber of Resonance', 11, 1, 'David Sterling', 275000, 8900000, 1.29),
        ('Fading Reflection', 11, 1, 'David Sterling', 230000, 7500000, 0.99),
        # Velvet Reverie - Silk and Strings (Classical - 7)
        ('Adagio in Blue', 12, 7, 'Clara Moreau', 320000, 10400000, 1.29),
        ('Prelude to Dawn', 12, 7, 'Clara Moreau', 195000, 6300000, 0.99),
        ('Nocturne No. 5', 12, 7, 'Clara Moreau', 270000, 8800000, 1.29),
        # Velvet Reverie - Nocturne Tales
        ('Sonata of Falling Leaves', 13, 7, 'Clara Moreau', 240000, 7800000, 0.99),
        ('Cello Rhapsody', 13, 7, 'Clara Moreau', 360000, 11700000, 1.29),
        # Apex Pulse - Pulse Core (Metal - 3)
        ('Iron Catalyst', 14, 3, 'Victor Stone, Kyle Reese', 305000, 9900000, 0.99),
        ('Obsidian Gate', 14, 3, 'Victor Stone', 480000, 15600000, 1.29),
        ('Steel Vortex', 14, 3, 'Victor Stone, Kyle Reese', 370000, 12000000, 0.99),
        # Apex Pulse - Overdrive Protocol
        ('Threshold of Fury', 15, 3, 'Victor Stone', 410000, 13300000, 1.29),
        ('Molten Core Run', 15, 3, 'Victor Stone', 295000, 9600000, 0.99),
        # Starlight Symphony - Celestial Harmony (Synthwave - 5)
        ('Constellation Drive', 16, 5, 'Seraphina Vance', 235000, 7600000, 1.29),
        ('Orbiting Mirrors', 16, 5, 'Seraphina Vance', 220000, 7100000, 0.99),
        ('Supernova Glow', 16, 5, 'Seraphina Vance', 245000, 8000000, 1.29),
        ('Lunar Halos', 16, 5, 'Seraphina Vance', 215000, 7000000, 0.99),
        # Starlight Symphony - Astral Wanderer
        ('Deep Nebula Drift', 17, 5, 'Seraphina Vance', 210000, 6800000, 1.29),
        ('Solar Flare Whisper', 17, 5, 'Seraphina Vance', 198000, 6400000, 0.99),
        # Terra Nova Collective - Earth and Sky (Hip Hop - 6)
        ('Cityscape Horizon', 18, 6, 'Kofi Mensah, Tariq Ali', 240000, 7800000, 1.29),
        ('Metropolitan Flow', 18, 6, 'Kofi Mensah', 225000, 7300000, 1.29),
        ('Midnight Asphalt', 18, 6, 'Kofi Mensah, Tariq Ali', 310000, 10100000, 0.99),
        # Terra Nova Collective - Roots and Rhythm
        ('Concrete Canvas', 19, 6, 'Kofi Mensah', 290000, 9400000, 0.99),
        ('Urban Rhythm Section', 19, 6, 'Kofi Mensah, Tariq Ali', 305000, 9900000, 1.29),
        # Cobalt Skies - Azure Horizons (Rock - 1)
        ('Stratosphere Skyline', 20, 1, 'Jordan Ross', 415000, 13500000, 1.29),
        ('Oceanic Meridian', 20, 1, 'Jordan Ross', 360000, 11700000, 1.29),
        ('Highland Vista', 20, 1, 'Jordan Ross', 430000, 14000000, 0.99),
        # Cobalt Skies - Endless Altitude
        ('Ascent to Cloudbase', 21, 1, 'Jordan Ross', 720000, 23400000, 1.29),
        ('Ridge Line Wind', 21, 1, 'Jordan Ross', 320000, 10400000, 1.29),
        # Luna Collective - Moonlight Serenade (Indie Folk - 9)
        ('Valley of Fireflies', 22, 9, 'Hannah Campbell', 230000, 7500000, 1.29),
        ('Autumn Cabin Songs', 22, 9, 'Hannah Campbell', 270000, 8800000, 1.29),
        ('Mountain River Run', 22, 9, 'Hannah Campbell', 235000, 7600000, 0.99),
        # Horizon Beat - Sunset Boulevard (Blues - 8)
        ('Delta River Cruise', 23, 8, 'Rayburn King', 245000, 8000000, 1.29),
        ('Backporch Shuffle', 23, 8, 'Rayburn King', 260000, 8500000, 0.99),
        ('Late Night Barstool', 23, 8, 'Rayburn King', 380000, 12400000, 1.29),
        # Prism Wave - Spectrum Odyssey (Ambient - 10)
        ('Ethereal Tide', 24, 10, 'Sora Takahashi', 280000, 9100000, 0.99),
        ('Aurora Cascade', 24, 10, 'Sora Takahashi', 310000, 10100000, 1.29),
        ('Infinite Horizon', 24, 10, 'Sora Takahashi', 350000, 11400000, 1.29)
    ]

    sql.append("-- 4. TRACKS")
    for tid, (name, alb_id, gid, comp, ms, b, price) in enumerate(tracks_data, 1):
        comp_val = f"'{comp}'" if comp else "NULL"
        sql.append(f"INSERT INTO tracks (track_id, name, album_id, genre_id, composer, milliseconds, bytes, unit_price) "
                   f"VALUES ({tid}, '{name}', {alb_id}, {gid}, {comp_val}, {ms}, {b}, {price:.2f});")
    sql.append("")

    # 5. EMPLOYEES
    employees = [
        (1, 'Adams', 'Andrew', 'General Manager', 'NULL', '1975-02-18', '2018-08-14', '11120 Jasper Ave NW', 'Edmonton', 'AB', 'Canada', 'T5K 2N1', '+1 (780) 428-9482', 'andrew@digitalmusic.com'),
        (2, 'Edwards', 'Nancy', 'Sales Manager', '1', '1982-12-08', '2019-05-01', '825 8 Ave SW', 'Calgary', 'AB', 'Canada', 'T2P 2T9', '+1 (403) 262-3443', 'nancy@digitalmusic.com'),
        (3, 'Peacock', 'Jane', 'Sales Support Agent', '2', '1988-08-29', '2020-04-01', '1111 6 Ave SW', 'Calgary', 'AB', 'Canada', 'T2P 5M5', '+1 (403) 262-3444', 'jane@digitalmusic.com'),
        (4, 'Park', 'Margaret', 'Sales Support Agent', '2', '1992-09-19', '2021-01-15', '683 10 Street SW', 'Calgary', 'AB', 'Canada', 'T2P 5G3', '+1 (403) 263-4423', 'margaret@digitalmusic.com'),
        (5, 'Johnson', 'Steve', 'Sales Support Agent', '2', '1990-03-03', '2021-10-17', '772 Cochrane Street', 'Calgary', 'AB', 'Canada', 'T2P 2P3', '+1 (403) 246-9887', 'steve@digitalmusic.com')
    ]
    sql.append("-- 5. EMPLOYEES")
    for emp in employees:
        rep = emp[4]
        sql.append(f"INSERT INTO employees (employee_id, last_name, first_name, title, reports_to, birth_date, hire_date, address, city, state, country, postal_code, phone, email) "
                   f"VALUES ({emp[0]}, '{emp[1]}', '{emp[2]}', '{emp[3]}', {rep}, '{emp[5]}', '{emp[6]}', '{emp[7]}', '{emp[8]}', '{emp[9]}', '{emp[10]}', '{emp[11]}', '{emp[12]}', '{emp[13]}');")
    sql.append("")

    # 6. CUSTOMERS (25 customers across several countries)
    customers = [
        (1, 'Luis', 'Goncalves', 'Embraer - Empresa Brasileira', 'Av. Brigadeiro Faria Lima, 2170', 'Sao Jose dos Campos', 'SP', 'Brazil', '12227-000', '+55 (12) 3923-5555', 'luisg@embraer.com.br', 3, '2024-01-10'),
        (2, 'Leonie', 'Kohler', 'NULL', 'Theodor-Heuss-Strasse 34', 'Stuttgart', 'BW', 'Germany', '70174', '+49 0711 2842222', 'leonie.kohler@surfeu.de', 5, '2024-01-15'),
        (3, 'Francois', 'Tremblay', 'NULL', '1498 rue Belanger', 'Montreal', 'QC', 'Canada', 'H2G 1A7', '+1 (514) 721-4711', 'ftremblay@gmail.com', 3, '2024-02-01'),
        (4, 'Bjorn', 'Hansen', 'NULL', 'Ullevålsveien 14', 'Oslo', 'NULL', 'Norway', '0171', '+47 22 44 22 22', 'bjorn.hansen@yahoo.no', 4, '2024-02-12'),
        (5, 'Frantisek', 'Wichterlova', 'NULL', 'Klanova 9/506', 'Prague', 'NULL', 'Czech Republic', '14700', '+420 2 4172 5555', 'frantisekw@seznam.cz', 4, '2024-02-20'),
        (6, 'Helena', 'Holy', 'NULL', 'Rilkeho 3174/6', 'Prague', 'NULL', 'Czech Republic', '14300', '+420 2 4177 0449', 'hholy@gmail.com', 5, '2024-03-05'),
        (7, 'Astrid', 'Gruber', 'NULL', 'Rotenturmstrasse 4, 1010 Innere Stadt', 'Vienna', 'NULL', 'Austria', '1010', '+43 01 5134477', 'astrid.gruber@apple.at', 5, '2024-03-15'),
        (8, 'Daan', 'Peeters', 'NULL', 'Rue Joseph Stevens 25', 'Brussels', 'NULL', 'Belgium', 'B-1000', '+32 02 512 3322', 'daan_peeters@apple.be', 4, '2024-03-22'),
        (9, 'Kara', 'Nielsen', 'NULL', 'Sønder Boulevard 51', 'Copenhagen', 'NULL', 'Denmark', '1720', '+45 33 25 34 66', 'kara.nielsen@jubii.dk', 4, '2024-04-02'),
        (10, 'Eduardo', 'Martins', 'Woodstock Discos', 'Rua da Assuncao 53', 'Lisbon', 'NULL', 'Portugal', 'NULL', '+351 (213) 466-111', 'eduardo@woodstock.pt', 4, '2024-04-10'),
        (11, 'Alexandre', 'Rocha', 'Banco do Brasil S.A.', 'Rua Dr. Falcao Filho, 155', 'Sao Paulo', 'SP', 'Brazil', '01007-010', '+55 (11) 3055-3278', 'alero@uol.com.br', 5, '2024-04-20'),
        (12, 'Roberto', 'Almeida', 'NULL', 'Praca Pio X, 119', 'Rio de Janeiro', 'RJ', 'Brazil', '20040-020', '+55 (21) 2271-7000', 'roberto.a@riotur.gov.br', 3, '2024-05-01'),
        (13, 'Fernanda', 'Ramos', 'NULL', 'QMS 6 Lote 40', 'Brasilia', 'DF', 'Brazil', '71576-400', '+55 (61) 3369-3201', 'fernr@terra.com.br', 4, '2024-05-15'),
        (14, 'Mark', 'Philips', 'Telus', '8210 111 ST NW', 'Edmonton', 'AB', 'Canada', 'T6G 2C7', '+1 (780) 434-4554', 'mphilips12@shaw.ca', 5, '2024-06-01'),
        (15, 'Jennifer', 'Peterson', 'Rogers Media', '700 W Pender Street', 'Vancouver', 'BC', 'Canada', 'V6C 1G8', '+1 (604) 688-2234', 'jenniferp@rogers.ca', 3, '2024-06-12'),
        (16, 'Frank', 'Harris', 'Google Inc.', '1600 Amphitheatre Parkway', 'Mountain View', 'CA', 'USA', '94043-1351', '+1 (650) 253-0000', 'fharris@google.com', 3, '2024-06-25'),
        (17, 'Jack', 'Smith', 'Microsoft Corporation', '1 Microsoft Way', 'Redmond', 'WA', 'USA', '98052-8300', '+1 (425) 882-8080', 'jacksmith@microsoft.com', 5, '2024-07-02'),
        (18, 'Michelle', 'Brooks', 'NULL', '627 Broadway', 'New York', 'NY', 'USA', '10012-2612', '+1 (212) 221-3546', 'michelleb@aol.com', 3, '2024-07-15'),
        (19, 'Tim', 'Goyer', 'Apple Inc.', '1 Infinite Loop', 'Cupertino', 'CA', 'USA', '95014', '+1 (408) 996-1010', 'tgoyer@apple.com', 3, '2024-08-01'),
        (20, 'Dan', 'Miller', 'NULL', '541 Del Medio Ave', 'Mountain View', 'CA', 'USA', '94040-111', '+1 (650) 644-3358', 'danmt@sbcglobal.net', 4, '2024-08-18'),
        (21, 'Kathy', 'Chase', 'NULL', '801 W 4th Street', 'Reno', 'NV', 'USA', '89503', '+1 (775) 223-7665', 'kachas@hotmail.com', 5, '2024-09-02'),
        (22, 'Heather', 'Leacock', 'NULL', '120 S Orange Ave', 'Orlando', 'FL', 'USA', '32801', '+1 (407) 999-7788', 'hleacock@gmail.com', 4, '2024-09-15'),
        (23, 'John', 'Gordon', 'NULL', '69 Salem Street', 'Boston', 'MA', 'USA', '2113', '+1 (617) 522-1333', 'johngordon22@yahoo.com', 3, '2024-10-01'),
        (24, 'Richard', 'Cunningham', 'NULL', '2211 W Berry Street', 'Fort Worth', 'TX', 'USA', '76110', '+1 (817) 924-7272', 'ricunningham@hotmail.com', 4, '2024-10-20'),
        (25, 'Patrick', 'Gray', 'NULL', '1033 N Park Ave', 'Tucson', 'AZ', 'USA', '85719', '+1 (520) 622-4200', 'patrick.gray@aol.com', 4, '2024-11-01')
    ]
    sql.append("-- 6. CUSTOMERS")
    for c in customers:
        comp = f"'{c[3]}'" if c[3] != 'NULL' else "NULL"
        state = f"'{c[6]}'" if c[6] != 'NULL' else "NULL"
        post = f"'{c[8]}'" if c[8] != 'NULL' else "NULL"
        sql.append(f"INSERT INTO customers (customer_id, first_name, last_name, company, address, city, state, country, postal_code, phone, email, support_rep_id, created_at) "
                   f"VALUES ({c[0]}, '{c[1]}', '{c[2]}', {comp}, '{c[4]}', '{c[5]}', {state}, '{c[7]}', {post}, '{c[9]}', '{c[10]}', {c[11]}, '{c[12]}');")
    sql.append("")

    # 7 & 8. INVOICES AND INVOICE_ITEMS
    start_date = datetime(2024, 1, 15)
    end_date = datetime(2026, 10, 25)
    delta_days = (end_date - start_date).days

    num_invoices = 85
    num_tracks = len(tracks_data)

    invoice_lines = []
    line_id = 1

    sql.append("-- 7. INVOICES & 8. INVOICE ITEMS")
    
    dates = sorted([start_date + timedelta(days=random.randint(0, delta_days), hours=random.randint(8, 22), minutes=random.randint(0, 59)) for _ in range(num_invoices)])

    customer_dict = {c[0]: c for c in customers}
    track_prices = {i: tracks_data[i-1][6] for i in range(1, num_tracks + 1)}

    for inv_id in range(1, num_invoices + 1):
        cust_weights = [3 if c[0] in (1, 3, 16, 17, 18, 22) else 1 for c in customers]
        cust_id = random.choices([c[0] for c in customers], weights=cust_weights, k=1)[0]
        cust = customer_dict[cust_id]
        inv_date = dates[inv_id - 1].strftime('%Y-%m-%d %H:%M:%S')

        count_tracks = random.choices([1, 2, 3, 4, 5, 6], weights=[20, 30, 25, 15, 7, 3], k=1)[0]
        chosen_tracks = random.sample(range(1, num_tracks + 1), count_tracks)

        inv_total = 0.0
        lines_for_this_inv = []
        for tid in chosen_tracks:
            price = track_prices[tid]
            qty = 1
            inv_total += price * qty
            lines_for_this_inv.append((line_id, inv_id, tid, price, qty))
            line_id += 1

        inv_total = round(inv_total, 2)
        billing_addr = cust[4].replace("'", "''")
        billing_city = cust[5].replace("'", "''")
        billing_state = f"'{cust[6]}'" if cust[6] != 'NULL' else "NULL"
        billing_country = cust[7]
        billing_postal = f"'{cust[8]}'" if cust[8] != 'NULL' else "NULL"

        sql.append(f"INSERT INTO invoices (invoice_id, customer_id, invoice_date, billing_address, billing_city, billing_state, billing_country, billing_postal_code, total) "
                   f"VALUES ({inv_id}, {cust_id}, '{inv_date}', '{billing_addr}', '{billing_city}', {billing_state}, '{billing_country}', {billing_postal}, {inv_total:.2f});")

        for lid, i_id, tid, uprice, qty in lines_for_this_inv:
            invoice_lines.append(f"INSERT INTO invoice_items (invoice_line_id, invoice_id, track_id, unit_price, quantity) VALUES ({lid}, {i_id}, {tid}, {uprice:.2f}, {qty});")

    sql.append("")
    sql.append("-- 8. INVOICE ITEMS")
    sql.extend(invoice_lines)
    sql.append("")

    # 9. PLAYLISTS
    playlists = [
        (1, 'Cosmic Rock Anthems'),
        (2, 'Midnight Synthwave Drive'),
        (3, 'Deep Space Ambient and Jazz'),
        (4, 'Acoustic and Classical Serenity'),
        (5, 'High Energy Workout Beats')
    ]
    sql.append("-- 9. PLAYLISTS")
    for pl_id, name in playlists:
        sql.append(f"INSERT INTO playlists (playlist_id, name) VALUES ({pl_id}, '{name}');")
    sql.append("")

    # 10. PLAYLIST TRACKS
    pl_mappings = [
        (1, 1), (1, 2), (1, 3), (1, 20), (1, 21), (1, 22), (1, 24), (1, 25), (1, 51), (1, 52),
        (2, 6), (2, 7), (2, 8), (2, 9), (2, 40), (2, 41), (2, 42), (2, 43),
        (3, 10), (3, 11), (3, 12), (3, 13), (3, 62), (3, 63), (3, 64),
        (4, 30), (4, 31), (4, 32), (4, 56), (4, 57), (4, 58),
        (5, 14), (5, 15), (5, 16), (5, 35), (5, 36), (5, 46), (5, 47)
    ]
    sql.append("-- 10. PLAYLIST TRACKS")
    for pl_id, tid in pl_mappings:
        sql.append(f"INSERT INTO playlist_tracks (playlist_id, track_id) VALUES ({pl_id}, {tid});")
    sql.append("")

    return "\n".join(sql)

if __name__ == '__main__':
    content = generate_seed_sql()
    seed_path = os.path.join(os.path.dirname(__file__), '..', 'seed_data.sql')
    with open(seed_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated {seed_path}")
