import sqlite3
import os
import sys

# DETERMINE PATH (Dev vs Prod)
if getattr(sys, 'frozen', False):
    base_dir = os.path.join(os.path.expanduser("~"), "Documents", "ProjectVault")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    DB_NAME = os.path.join(base_dir, "vault.db")
else:
    DB_NAME = os.path.join(os.path.dirname(__file__), "vault.db")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT,
            status TEXT,
            budget REAL
        )
    ''')
    
    # ADDED: category COLUMN
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            description TEXT NOT NULL,
            category TEXT, 
            amount REAL,
            date TEXT,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[DB] Database initialized with Categories.")

init_db()