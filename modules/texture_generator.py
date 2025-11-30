import os
import numpy as np
from scipy.io.wavfile import write as write_wav
import time

def generate_texture(duration_seconds=16, sr=44100):
    """
    Génère une texture sonore (Bruit Rose simulé) pour donner de la profondeur au mix.
    """
    print("   🔊 Génération d'une texture sonore (Ambience Layer)...")
    
    # Génération de bruit blanc
    noise = np.random.randn(sr * duration_seconds)
    
    # Application d'un filtre simple pour le transformer en bruit "Rose" (plus doux, moins agressif)
    # Algorithme Voss-McCartney simplifié ou filtrage basique
    b = [0.049922035, -0.095993537, 0.050644005, -0.004408786]
    a = [1.0, -2.494956166, 2.017265875, -0.522189064]
    
    # Initialisation
    output = np.zeros_like(noise)
    
    # Simulation de filtrage (Low Pass) via moyenne mobile pour éviter scipy.signal complexe
    # On lisse le bruit pour enlever les aigus criards
    output = np.convolve(noise, np.ones(50)/50, mode='same')

    # Normalisation du volume (très bas, c'est un fond)
    # On le met à 15% du volume max
    if np.max(np.abs(output)) > 0:
        output = output / np.max(np.abs(output)) * 0.15
    
    # Création du chemin
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'output')
    
    # On s'assure que le dossier existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    texture_path = os.path.join(output_dir, f'texture_{int(time.time())}.wav')
    
    # Sauvegarde
    write_wav(texture_path, sr, output.astype(np.float32))
    
    return texture_path

# Test local
if __name__ == "__main__":
    generate_texture()