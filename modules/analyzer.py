import librosa
import numpy as np
import os

def analyze_track(file_path):
    """Extrait les caractéristiques audio (Features)."""
    
    try:
        # 1. Chargement du fichier audio
        y, sr = librosa.load(file_path)
        
        # 2. Extraction de Features (Le cœur du métier Data Scientist Audio)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = np.mean(librosa.feature.rms(y=y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        # 3. Rapport d'analyse
        return {
            "bpm": round(float(tempo[0]), 1) if isinstance(tempo, np.ndarray) else round(float(tempo), 1),
            "rms": round(float(rms), 4),
            "spectral_centroid": round(float(centroid), 1)
        }

    except Exception as e:
        print(f"   ❌ ERREUR ANALYSE : {e}")
        return None