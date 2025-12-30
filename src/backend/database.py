import sqlite3
import os
import sys

# DETERMINE PATH:
# If frozen (running as exe), use Documents folder.
# If dev (running script), use current folder.
if getattr(sys, 'frozen', False):
    # We are running as a compiled exe
    # Save to: C:\Users\Hector\Documents\ProjectVault\vault.db
    base_dir = os.path.join(os.path.expanduser("~"), "Documents", "ProjectVault")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    DB_NAME = os.path.join(base_dir, "vault.db")
else:
    # We are in Dev mode
    DB_NAME = os.path.join(os.path.dirname(__file__), "vault.db")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT,
            status TEXT,
            budget REAL
        )
    ''')
    
    # 2. Transactions Table (This is the one you were missing!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            description TEXT NOT NULL,
            amount REAL,
            date TEXT,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized.")

# Run initialization immediately when imported
init_db()