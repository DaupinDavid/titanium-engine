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

# Initialisation BDD
database.init_db()

st.title("🎵 Titanium Data Engine")
st.markdown("### Générateur Audio Autonome & Analytique (Niveau 10/10)")

# --- BARRE LATÉRALE (Contrôles) ---
with st.sidebar:
    st.header("🎛️ Commandes")
    
    if st.button("🚀 LANCER LA PRODUCTION", type="primary"):
        with st.spinner('Fabrication & Analyse en cours... (Cela peut prendre 1 min)'):
            final_file = main.run_pipeline() # Déclenche tout le pipeline
            
            if final_file:
                st.session_state['last_track'] = os.path.join(base_dir, 'output', final_file)
                # Force le rechargement pour voir le nouveau track dans le tableau
                time.sleep(1) 
                st.rerun()
            else:
                 st.error("Échec du pipeline. Regardez l'onglet 'Logs' sur le site Render pour voir l'erreur exacte.")

# --- ZONE PRINCIPALE ---
col1, col2 = st.columns([1, 2])

# Colonne 1 : Lecteur
with col1:
    st.subheader("🎧 Dernier Track")
    
    if 'last_track' in st.session_state and os.path.exists(st.session_state['last_track']):
        st.success("Track généré !")
        st.audio(st.session_state['last_track'])
        
        try:
            conn = sqlite3.connect(db_path)
            df_last = pd.read_sql_query("SELECT bpm, status FROM generations ORDER BY id DESC LIMIT 1", conn)
            conn.close()
            
            if not df_last.empty:
                bpm_val = df_last['bpm'].iloc[0]
                status_val = df_last['status'].iloc[0]
                c1, c2 = st.columns(2)
                c1.metric("BPM", bpm_val)
                c2.metric("Statut", status_val)
        except:
             pass
    else:
        st.info("Cliquez sur LANCER pour commencer.")

# Colonne 2 : Historique
with col2:
    st.subheader("🗄️ Historique de Production (SQL)")
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT id, timestamp, filename, bpm, status FROM generations ORDER BY id DESC LIMIT 15", conn)
        
        # --- CORRECTION ICI : On utilise l'option standard ---
        st.dataframe(df, use_container_width=True) 
        # -----------------------------------------------------
        
        conn.close()
    except Exception as e:
        st.warning(f"Base de données en attente... ({e})")