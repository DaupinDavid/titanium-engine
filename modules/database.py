import sqlite3
import os
from datetime import datetime

# Nom de la base de données
DB_NAME = "tracks.db"

def get_db_path():
    """Retourne le chemin absolu vers la base de données à la racine."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DB_NAME)

def init_db():
    """Crée la table si elle n'existe pas encore."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Création de la table SQL
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
    print(f"   🗄️  Base de données connectée : {db_path}")

def log_track(filename, bpm, key, status="SUCCESS"):
    """Insère une ligne dans le registre."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO generations (timestamp, filename, bpm, key, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, filename, bpm, key, status))
    
    conn.commit()
    conn.close()
    print(f"   📝 Track loggé en base : {filename}")

# --- TEST LOCAL ---
if __name__ == "__main__":
    # On teste la création de la table et l'insertion d'une ligne bidon
    init_db()
    log_track("test_audio.wav", 128, "C Minor", "TEST_MANUEL")