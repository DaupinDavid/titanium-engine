import time
import pandas as pd
import sqlite3
import os
import main # On importe la fonction run_pipeline()
from modules import database # Nécessaire pour les chemins de la BDD

# Configuration
NUM_RUNS = 5
SCORE_THRESHOLD = 75 

def run_factory():
    print(f"\n🏭 Démarrage de l'Usine APEX FORGE : {NUM_RUNS} cycles")
    
    # 1. Exécuter les cycles de production
    for i in range(NUM_RUNS):
        print(f"\n--- CYCLE {i+1}/{NUM_RUNS} : Début de la génération ---")
        main.run_pipeline() # Déclenche le pipeline complet
        time.sleep(1) # Pause pour éviter le sur-usage CPU

    # 2. Récupérer les résultats du Scoring et Filtrer
    database.init_db() # Assurer que la table est là (pour le cas où elle aurait été supprimée)
    db_path = database.get_db_path() 
    conn = sqlite3.connect(db_path)
    
    # Sélectionner les pistes réussies (High Quality) loggées
    df = pd.read_sql_query(f"""
        SELECT filename, status, bpm
        FROM generations 
        WHERE status LIKE 'SUCCESS%'
        ORDER BY id DESC LIMIT {NUM_RUNS} 
    """, conn)
    
    conn.close()

    print("\n--- ✅ ANALYSE FINALE DES CYCLES ---")
    
    if df.empty:
        print("\n❌ ÉCHEC : Aucune piste valide générée.")
        return

    # 3. Le Vrai Jugement (Filtrage)
    # On filtre les résultats loggés par le statut HIGH_Q (qui est > 75)
    high_q_tracks = df[df['status'] == 'SUCCESS_HIGH_Q']
    
    print(f"Total des pistes générées : {len(df)}")
    print(f"Pistes ayant atteint le niveau HIGH_Q (Score >= {SCORE_THRESHOLD}) : {len(high_q_tracks)}")
    
    if not high_q_tracks.empty:
        best_track = high_q_tracks.iloc[0]['filename']
        best_bpm = high_q_tracks.iloc[0]['bpm']
        print(f"\n👑 MEILLEURE PISTE APEX (Qualité A) : {best_track} ({best_bpm} BPM)")
        print("   Ce fichier WAV est le produit final pour votre portfolio.")
    else:
        print("\n⚠️ Aucune piste n'a atteint le seuil de haute qualité (Score < 75).")
        print("   Veuillez relancer la production.")

if __name__ == "__main__":
    database.init_db() # Initialisation de la BDD au démarrage du script
    run_factory()