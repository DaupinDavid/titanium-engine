import streamlit as st
import pandas as pd
import sqlite3
import os
import time
from modules import composer, synthesizer, database, dsp, analyzer

# Configuration de la page
st.set_page_config(page_title="Titanium AI Audio", page_icon="🎵", layout="wide")

st.title("🎵 Titanium Data Engine")
st.markdown("### Générateur Audio Autonome & Analytique")

# Barre latérale pour les contrôles
with st.sidebar:
    st.header("🎛️ Paramètres")
    bpm_target = st.slider("Cible BPM", 80, 160, 120)
    st.info("Le moteur choisira une variation autour de cette cible.")
    
    if st.button("🚀 LANCER LA PRODUCTION", type="primary"):
        with st.spinner('Composition & Synthèse en cours...'):
            # 1. SETUP
            database.init_db()
            timestamp = int(time.time())
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
            midi_name = f"track_{timestamp}.mid"
            wav_name = f"track_{timestamp}.wav"
            final_name = f"master_{timestamp}.wav"
            
            midi_path = os.path.join(output_dir, midi_name)
            wav_path = os.path.join(output_dir, wav_name)
            final_path = os.path.join(output_dir, final_name)

            # 2. PIPELINE COMPLET
            # A. Composition
            status_text = st.empty()
            status_text.text("🎼 Écriture de la partition...")
            score, real_bpm = composer.generate_melody() 
            score.write('midi', fp=midi_path)
            
            # B. Synthèse
            status_text.text("🎹 Rendu Audio (FluidSynth)...")
            synthesizer.render_wav(midi_path, wav_path)
            
            # C. Mastering (DSP)
            status_text.text("🎚️ Mastering (Pedalboard)...")
            dsp.master_track(wav_path, final_path)
            
            # D. Analyse (Data)
            status_text.text("🔍 Analyse Data (Librosa)...")
            features = analyzer.analyze_track(final_path)
            
            # E. Logging
            database.log_track(final_name, real_bpm, "C Minor", "SUCCESS")
            
            status_text.success(f"✅ Terminé ! ({real_bpm} BPM)")
            
            # Mise en session pour affichage immédiat
            st.session_state['last_track'] = final_path
            st.session_state['last_features'] = features

# ZONE PRINCIPALE
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎧 Dernier Track")
    if 'last_track' in st.session_state:
        st.audio(st.session_state['last_track'])
        
        # Affichage des métriques sous forme de "Cartes"
        feats = st.session_state.get('last_features', {})
        if feats:
            c1, c2, c3 = st.columns(3)
            c1.metric("BPM", feats.get('bpm', '-'))
            c2.metric("RMS (Vol)", feats.get('rms', '-'))
            c3.metric("Brillance", feats.get('spectral_centroid', '-'))
    else:
        st.info("Aucun track généré pour l'instant.")

with col2:
    st.subheader("🗄️ Historique de Production (SQL)")
    # Connexion à la BDD pour afficher le tableau
    try:
        conn = sqlite3.connect("tracks.db")
        df = pd.read_sql_query("SELECT id, timestamp, filename, bpm, status FROM generations ORDER BY id DESC LIMIT 10", conn)
        # CORRECTION ICI : On a enlevé le paramètre qui fâchait
        st.dataframe(df)
        conn.close()
    except:
        st.warning("Base de données vide ou inaccessible.")