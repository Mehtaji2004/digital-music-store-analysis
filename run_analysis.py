#!/usr/bin/env python3
"""
Digital Music Store Analytics Runner
Executes analytical SQL query files on the music_store.db database,
displays formatted ASCII tables in the terminal, and exports a comprehensive
markdown report to outputs/query_results_summary.md.
"""

import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "music_store.db")
QUERIES_DIR = os.path.join(BASE_DIR, "queries")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

QUERY_FILES = [
    ("01_exploratory_data_analysis.sql", "Exploratory Data Analysis (EDA)"),
    ("02_sales_and_revenue_metrics.sql", "Sales & Revenue Business Intelligence"),
    ("03_advanced_analytics.sql", "Advanced Analytics & Window Functions"),
    ("04_rfm_customer_segmentation.sql", "RFM Customer Segmentation & Strategy"),
]

def ensure_database():
    """Builds the database if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        print("--> Database not found. Building music_store.db from schema.sql and seed_data.sql...")
        schema_path = os.path.join(BASE_DIR, "schema.sql")
        seed_path = os.path.join(BASE_DIR, "seed_data.sql")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        with open(seed_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
        print("--> Database successfully initialized!")

def format_table_markdown(headers, rows):
    """Formats rows as a Markdown table."""
    if not headers:
        return ""
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val if val is not None else "NULL")))

    header_line = "| " + " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths)) + " |"
    separator_line = "| " + " | ".join("-" * w for w in col_widths) + " |"
    data_lines = [
        "| " + " | ".join(str(v if v is not None else "NULL").ljust(w) for v, w in zip(row, col_widths)) + " |"
        for row in rows
    ]
    return "\n".join([header_line, separator_line] + data_lines)

def run_queries():
    ensure_database()
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    report_path = os.path.join(OUTPUTS_DIR, "query_results_summary.md")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    report_lines = [
        "# Digital Music Store Analysis - Query Results Summary",
        "\n*Generated automatically from `run_analysis.py` on SQLite database.*\n",
        "This document contains live executed outputs for all analytical SQL queries in the project.\n"
    ]

    for file_name, suite_title in QUERY_FILES:
        file_path = os.path.join(QUERIES_DIR, file_name)
        if not os.path.exists(file_path):
            continue

        print(f"\n{'='*70}\n[SUITE] {suite_title}\nFile: queries/{file_name}\n{'='*70}")
        report_lines.append(f"## {suite_title} (`queries/{file_name}`)\n")

        with open(file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Split statements by semicolon at the end of a line (ignores semicolons inside string literals)
        import re
        raw_queries = [q.strip() for q in re.split(r';\s*(?:\n|$)', sql_script) if q.strip()]

        q_num = 1
        for raw_q in raw_queries:
            # Extract header comment if present
            comment_lines = []
            code_lines = []
            for line in raw_q.split("\n"):
                if line.strip().startswith("--"):
                    comment_lines.append(line.strip().lstrip("-").strip())
                else:
                    code_lines.append(line)

            query_code = "\n".join(code_lines).strip()
            if not query_code:
                continue

            title = f"Query {q_num}"
            for c in comment_lines:
                if "Objective:" in c or "Q" in c:
                    title = c
                    break

            print(f"\n--- {title} ---")
            report_lines.append(f"### {title}\n")
            if comment_lines:
                desc = " ".join([c for c in comment_lines if not c.startswith("Q") and not c.startswith("---")])
                if desc:
                    report_lines.append(f"> **Notes**: {desc}\n")

            report_lines.append("```sql\n" + query_code + "\n```\n")

            try:
                cursor.execute(query_code)
                headers = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()

                # Print first 5 rows to stdout
                print(f"Columns: {', '.join(headers)}")
                print(f"Total Rows: {len(rows)}")
                for r in rows[:5]:
                    print("  ", r)
                if len(rows) > 5:
                    print(f"  ... ({len(rows) - 5} more rows)")

                # Markdown table for report (limit 15 rows for readability if huge)
                display_rows = rows[:20]
                md_table = format_table_markdown(headers, display_rows)
                report_lines.append(md_table)
                if len(rows) > 20:
                    report_lines.append(f"\n*Showing top 20 of {len(rows)} rows.*\n")
                else:
                    report_lines.append("\n")

            except sqlite3.Error as e:
                print(f"Error executing query: {e}")
                report_lines.append(f"**Error**: `{e}`\n")

            q_num += 1

    conn.close()

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n{'='*70}\n[SUCCESS] Comprehensive markdown report written to:\n{report_path}\n{'='*70}\n")

if __name__ == "__main__":
    run_queries()
