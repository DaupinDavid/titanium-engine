import streamlit as st
import pandas as pd
import sqlite3
import os
import time
from modules import composer, synthesizer, database, dsp, analyzer
import main 

# Configuration de la page
st.set_page_config(page_title="Titanium AI Audio", page_icon="🎵", layout="wide")

# Définition des chemins
DB_NAME = "tracks.db"
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, DB_NAME)

st.title("🎵 Titanium Data Engine")
st.markdown("### Générateur Audio Autonome & Analytique (Niveau 10/10)")

# --- BARRE LATÉRALE (Contrôles) ---
with st.sidebar:
    st.header("🎛️ Commandes")
    
    if st.button("🚀 LANCER LA PRODUCTION", type="primary"):
        with st.spinner('Fabrication & Analyse en cours...'):
            final_file = main.run_pipeline() # Déclenche tout le pipeline
            
            if final_file:
                # Stocker le chemin du fichier pour le lecteur audio
                st.session_state['last_track'] = os.path.join(base_dir, 'output', final_file)
            else:
                 st.error("Échec du pipeline. Vérifiez les logs.")

# --- ZONE PRINCIPALE ---
col1, col2 = st.columns([1, 2])

# Colonne 1 : Lecteur et Statistiques
with col1:
    st.subheader("🎧 Dernier Track")
    
    # Affichage de l'audio si disponible
    if 'last_track' in st.session_state and os.path.exists(st.session_state['last_track']):
        st.success("Track généré et analysé!")
        st.audio(st.session_state['last_track'])
        
        # Récupération des dernières stats de la BDD pour l'affichage
        try:
            conn = sqlite3.connect(db_path)
            # On récupère le dernier BPM loggé
            df_last = pd.read_sql_query("SELECT bpm, status FROM generations ORDER BY id DESC LIMIT 1", conn)
            
            if not df_last.empty:
                bpm_val = df_last['bpm'].iloc[0]
                status_val = df_last['status'].iloc[0]

                c1, c2 = st.columns(2)
                c1.metric("BPM", bpm_val)
                c2.metric("Statut", status_val)
        except:
             st.info("Statistiques prêtes après le premier clic.")

    else:
        st.info("Cliquez sur LANCER LA PRODUCTION pour commencer.")

# Colonne 2 : Historique et Dataframe SQL
with col2:
    st.subheader("🗄️ Historique de Production (SQL)")
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT id, timestamp, filename, bpm, status FROM generations ORDER BY id DESC LIMIT 15", conn)
        
        # Correction pour Streamlit (enlève le paramètre déprécié)
        st.dataframe(df, width=None) 
        conn.close()
    except Exception as e:
        st.warning(f"Base de données inaccessible ou vide. (Erreur: {e})")