import sqlite3
import os
from datetime import datetime

DB_NAME = "tracks.db"

def get_db_path():
    """Retourne le chemin absolu vers la base de données à la racine."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DB_NAME)

def connect_db():
    """Établit et retourne la connexion à la base de données."""
    db_path = get_db_path()
    return sqlite3.connect(db_path)

def init_db():
    """Crée la table si elle n'existe pas encore (nécessaire au démarrage du dashboard)."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            bpm INTEGER,
            key TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_track(filename, bpm, key, status="SUCCESS"):
    """Insère une ligne dans le registre."""
    conn = connect_db()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO generations (timestamp, filename, bpm, key, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, filename, bpm, key, status))
    
    conn.commit()
    conn.close()