import os
import time
from modules import composer, synthesizer, database, dsp, analyzer
import shutil # Pour supprimer les fichiers temporaires

def run_pipeline():
    print("🚀 Démarrage du pipeline TITANIUM...")

    # 1. INITIALISATION & SETUP
    database.init_db()
    timestamp = int(time.time())
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'output')
    
    # --- FIX CRITIQUE : Crée le dossier 'output' s'il n'existe pas (pour Docker) ---
    os.makedirs(output_dir, exist_ok=True)
    
    midi_filename = f"track_{timestamp}.mid"
    wav_raw_filename = f"track_raw_{timestamp}.wav"
    wav_master_filename = f"master_{timestamp}.wav"
    
    midi_path = os.path.join(output_dir, midi_filename)
    raw_wav_path = os.path.join(output_dir, wav_raw_filename)
    final_wav_path = os.path.join(output_dir, wav_master_filename)

    # 2. COMPOSITION (Cerveau)
    score, bpm = composer.generate_melody()
    score.write('midi', fp=midi_path)

    # 3. SYNTHÈSE (Moteur)
    synth_success = synthesizer.render_wav(midi_path, raw_wav_path)
    
    if not synth_success:
        database.log_track(wav_master_filename, bpm, "C Minor", "FAILED_SYNTH")
        return False
        
    # 4. MASTERING (Qualité)
    dsp_success = dsp.master_track(raw_wav_path, final_wav_path)
    
    # 5. ANALYSE (Data Scientist)
    features = analyzer.analyze_track(final_wav_path)

    # 6. ENREGISTREMENT (Mémoire)
    if dsp_success and features:
        key = composer.load_config()['generation_settings']['default_key']
        
        # On pourrait logguer les features ici aussi si on ajoutait les colonnes à la BDD
        database.log_track(wav_master_filename, bpm, key, "SUCCESS")
        
        # NOTE : On supprime le MIDI et le WAV RAW (on ne garde que le master final)
        os.remove(midi_path)
        os.remove(raw_wav_path)
        
        print(f"   ✅ PIPELINE TERMINÉ ! Fichier final : {wav_master_filename}")
        return wav_master_filename

    else:
        database.log_track(wav_master_filename, bpm, "Unknown", "FAILED_DSP")
        return False

if __name__ == "__main__":
    run_pipeline()