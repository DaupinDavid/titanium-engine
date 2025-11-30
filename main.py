import os
import time
from datetime import datetime
from modules import composer, synthesizer, database, dsp, analyzer, humanizer, arranger, texture_generator

def run_pipeline():
    print("\n--- 🚀 TITANIUM APEX : DÉMARRAGE ---")
    
    # 1. SETUP
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    ts = datetime.now().strftime("%H%M%S")
    path_midi = os.path.join(output_dir, f"track_{ts}.mid")
    path_raw = os.path.join(output_dir, f"raw_{ts}.wav")
    path_final = os.path.join(output_dir, f"MASTER_{ts}.wav")
    
    # BDD
    database.init_db()
    
    # 2. GENERATION TEXTURE
    path_texture = texture_generator.generate_texture(duration_seconds=30)

    # 3. COMPOSITION
    print("   🎶 Composition...")
    score, bpm = composer.generate_melody()
    score = humanizer.humanize_score(score)
    score.write('midi', fp=path_midi)
    
    # 4. SYNTHESE (Safe Mode)
    # Note: le soundfont est hardcodé dans synthesizer.py pour la sécurité C:\SF2
    success = synthesizer.render_wav(path_midi, "dummy", path_raw)
    
    if not success:
        print("   ⛔ STOP : Synthèse échouée.")
        return

    # 5. MIXAGE
    dsp.master_track(path_raw, path_texture, path_final)
    
    # 6. ANALYSE
    feats = analyzer.analyze_track(path_final)
    score_q = feats.get('score_index', 0)
    
    print(f"   🏆 SCORE QUALITÉ : {score_q}/100")
    print(f"   ✅ TERMINÉ : {path_final}")

if __name__ == "__main__":
    run_pipeline()