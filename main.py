import os
import time
from datetime import datetime
import json
import shutil 

# Import des modules
from modules import composer, synthesizer, database, dsp, analyzer, humanizer, arranger, texture_generator

# --- Fonctions utilitaires ---
def get_file_paths():
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    midi_filename = f"track_{timestamp}.mid"
    wav_filename = f"track_master_{timestamp}.wav"
    
    return {
        'base_path': base_path,
        'config_path': os.path.join(base_path, 'config.json'),
        'midi_path': os.path.join(output_dir, midi_filename),
        'wav_path': os.path.join(output_dir, wav_filename),
        'midi_filename': midi_filename,
        'wav_filename': wav_filename,
    }

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

# --- PIPELINE PRINCIPAL ---
def run_pipeline():
    print("--- ⚙️ TITANIUM CORE : LANCEMENT DU PIPELINE ---")
    start_time = time.time()
    
    paths = get_file_paths()
    config = load_config(paths['config_path'])
    
    # 1. SETUP
    database.init_db() 
    conn = database.connect_db() 
    print("   ✅ Configuration et Connexion BDD OK.")

    # Définition des fichiers temporaires pour le mixage texture
    temp_raw_midi = paths['midi_path']
    # On crée un nom unique pour le raw
    temp_raw_wav = os.path.join(paths['base_path'], 'output', f"raw_{paths['midi_filename'].replace('.mid', '.wav')}")
    
    # --- PHASE 6 : GÉNÉRATION TEXTURE ---
    # On génère une texture de la durée approximative (24 mesures * 4 temps / 120 BPM * 60s ~ 48s)
    # On met 20 secondes par défaut pour couvrir large
    texture_path = texture_generator.generate_texture(duration_seconds=25)
    
    try:
        # 2. COMPOSITION (Cerveau V6)
        print("   🎶 Génération du score musical...")
        score, bpm = composer.generate_melody()
        
        # Humanisation & Arrangement
        score = humanizer.humanize_score(score)
        score = arranger.create_full_arrangement(score)
        
        score.write('midi', fp=temp_raw_midi)
        print(f"   🎼 MIDI généré : {paths['midi_filename']} ({bpm} BPM)")
        
        # 3. SYNTHESE (Moteur FluidSynth)
        sf2_rel_path = config['paths']['soundfont']
        # Utilisation de os.path.normpath pour gérer les slashs Windows/Linux automatiquement
        soundfont_path = os.path.normpath(os.path.join(paths['base_path'], sf2_rel_path))

        synth_success = synthesizer.render_wav(temp_raw_midi, soundfont_path, temp_raw_wav)
        
        if not synth_success:
            print("   ❌ ARRÊT : La synthèse audio a échoué.")
            return

        # 4. MASTERING & MIXAGE (DSP Bipiste)
        # On mixe le RAW (FluidSynth) avec la TEXTURE
        dsp.master_track(temp_raw_wav, texture_path, paths['wav_path'])
        print("   🎚️ Mixage Texture + Mastering DSP appliqué.")
        
        # 5. ANALYSE & LOGGING
        features = analyzer.analyze_track(paths['wav_path'])
        score_index = features.get('score_index', 0)
        final_status = "SUCCESS_HIGH_Q" if score_index >= 75 else "SUCCESS_LOW_Q"
        
        key = config.get('generation_settings', {}).get('default_key', 'N/A')
        database.log_track(paths['wav_filename'], bpm, key, final_status)
        
        # --- NETTOYAGE DÉSACTIVÉ POUR DEBUG ---
        # Si tu veux garder les fichiers preuves, laisse ces lignes commentées
        # if os.path.exists(temp_raw_midi): os.remove(temp_raw_midi)
        # if os.path.exists(temp_raw_wav): os.remove(temp_raw_wav)
        # if os.path.exists(texture_path): os.remove(texture_path)
        # --------------------------------------
        
    except Exception as e:
        print(f"   ❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc() # Affiche le détail complet de l'erreur pour comprendre
        return

    # 6. CONCLUSION
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f"\n--- ✅ PIPELINE TERMINÉ en {duration} secondes ---")
    print(f"Fichier final : {paths['wav_path']}")

if __name__ == "__main__":
    run_pipeline()