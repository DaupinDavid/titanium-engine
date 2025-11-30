import os
import time
from modules import composer, synthesizer, database

def run_pipeline():
    print("🚀 Démarrage du pipeline TITANIUM...")

    # 1. INITIALISATION
    # On s'assure que la base de données est prête
    database.init_db()
    
    # On prépare les noms de fichiers (Timestamp unique)
    timestamp = int(time.time())
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    midi_filename = f"track_{timestamp}.mid"
    wav_filename = f"track_{timestamp}.wav"
    
    midi_path = os.path.join(output_dir, midi_filename)
    wav_path = os.path.join(output_dir, wav_filename)

    # 2. COMPOSITION (Cerveau)
    try:
        score, bpm = composer.generate_melody()
        # On sauvegarde le MIDI
        score.write('midi', fp=midi_path)
        print(f"   🎼 MIDI généré : {midi_filename} ({bpm} BPM)")
    except Exception as e:
        print(f"   ❌ ERREUR COMPOSITION : {e}")
        return

    # 3. SYNTHÈSE (Moteur)
    success = synthesizer.render_wav(midi_path, wav_path)
    
    # 4. ENREGISTREMENT (Mémoire)
    if success:
        # On note le succès dans la BDD
        # Note : On récupère la tonalité depuis la config (simplification pour l'instant)
        config = composer.load_config()
        key = config['generation_settings']['default_key']
        
        database.log_track(wav_filename, bpm, key, "SUCCESS")
        print(f"   ✅ TERMINÉ ! Fichier final : {wav_path}")
    else:
        database.log_track(midi_filename, bpm, "Unknown", "FAILED")
        print("   ⚠️ Pipeline terminé avec des erreurs audio.")

if __name__ == "__main__":
    run_pipeline()