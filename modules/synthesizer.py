import os
import subprocess
import json
import sys

def load_config():
    """Charge la configuration, nécessaire pour trouver le SoundFont."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # En production, on veut une erreur propre si config manque
        print("❌ ERREUR FATALE: config.json introuvable.")
        sys.exit(1)


def render_wav(midi_path, output_wav_path):
    """
    Convertit un fichier MIDI en WAV en utilisant FluidSynth.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = load_config()
    
    # --- DÉTECTION DE L'EXÉCUTABLE (Gère Windows et Linux/Cloud) ---
    # Sur Linux/Docker, l'exe est juste 'fluidsynth' dans le PATH.
    # Sur Windows, on utilise le chemin portable.
    if os.name == 'nt':
        # NOTE: Le chemin dépend de l'extraction faite par l'utilisateur
        fluidsynth_exe = os.path.join(base_dir, 'fluidsynth', 'bin', 'fluidsynth.exe')
    else:
        fluidsynth_exe = 'fluidsynth' # Docker/Linux PATH
        
    sf2_rel_path = config['paths']['soundfont']
    soundfont_path = os.path.join(base_dir, sf2_rel_path.replace('/', os.sep))

    # Vérification de la SoundFont (le carburant)
    if not os.path.exists(soundfont_path):
        print(f"❌ ERREUR : Soundfont introuvable : {soundfont_path}")
        return False

    # La Commande Magique
    cmd = [
        fluidsynth_exe,
        '-ni',              # No Interface
        '-g', '1.0',        # Gain
        '-F', output_wav_path, # Sortie WAV
        soundfont_path,     # Banque de sons
        midi_path           # Fichier d'entrée
    ]

    # Exécution silencieuse
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False