import librosa
import numpy as np
import os

def calculate_score(rms, bpm, centroid):
    """
    Calcule un indice de qualité simple (sur 100) basé sur les métriques audio.
    Un bon score nécessite un volume (RMS) élevé et une certaine complexité (Centroid).
    """
    # Score de volume (RMS) : Plus c'est fort, mieux c'est (max 0.15)
    score_rms = min(1.0, rms / 0.15) * 50 
    
    # Score de complexité/clarté (Centroid) : Pénalité si trop grave ou trop aigu
    score_centroid = (1.0 - abs(centroid - 1500) / 1000) * 50
    
    final_score = max(0, min(100, score_rms + score_centroid))
    return round(final_score, 1)

def analyze_track(file_path):
    """Extrait les caractéristiques audio (Features) et calcule le Score."""
    
    try:
        y, sr = librosa.load(file_path)
        
        # Extraction de Features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = np.mean(librosa.feature.rms(y=y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        # Calcul du Score
        score_index = calculate_score(rms, float(tempo[0]), np.mean(centroid))
        
        # Rapport d'analyse
        return {
            "bpm": round(float(tempo[0]), 1),
            "rms": round(float(rms), 4),
            "spectral_centroid": round(float(centroid), 1),
            "score_index": score_index
        }

    except Exception as e:
        print(f"   ❌ ERREUR ANALYSE : {e}")
        return None