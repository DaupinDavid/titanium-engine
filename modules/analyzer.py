import librosa
import numpy as np
import os

def analyze_track(file_path):
    """
    Extrait les caractéristiques audio (Features) du fichier pour l'analyse Data.
    """
    print(f"   🔍 Analyse Data en cours : {os.path.basename(file_path)}")
    
    try:
        # 1. Chargement du fichier audio en tableau Numpy (Série temporelle)
        # y = amplitude du signal, sr = sample rate
        y, sr = librosa.load(file_path)
        
        # 2. Extraction de Features (Le cœur du métier Data Scientist Audio)
        
        # Tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # Note : tempo est souvent un tableau, on prend la valeur scalaire
        bpm_detected = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

        # RMS (Root Mean Square) = Puissance/Volume moyen
        rms = np.mean(librosa.feature.rms(y=y))
        
        # Spectral Centroid = "Centre de gravité" du spectre (Brillance du son)
        spec_cent = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        # 3. Rapport d'analyse
        print(f"      📈 Tempo détecté (IA) : {bpm_detected:.1f} BPM")
        print(f"      🔊 Volume moyen (RMS) : {rms:.4f}")
        print(f"      ✨ Brillance spectrale : {spec_cent:.1f} Hz")
        
        return {
            "bpm": round(bpm_detected, 1),
            "rms": round(rms, 4),
            "spectral_centroid": round(spec_cent, 1)
        }

    except Exception as e:
        print(f"   ❌ ERREUR ANALYSE : {e}")
        return None

# --- TEST LOCAL ---
if __name__ == "__main__":
    # On teste sur le fichier masterisé
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_wav = os.path.join(base, 'output', 'test_audio_mastered.wav')
    
    if os.path.exists(target_wav):
        analyze_track(target_wav)
    else:
        print("⚠️ Fichier introuvable. Lance dsp.py d'abord !")