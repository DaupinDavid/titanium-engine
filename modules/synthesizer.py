import os
import subprocess
import json

def load_config():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def render_wav(midi_path, output_wav_path):
    """
    Convertit un fichier MIDI en WAV en utilisant le moteur FluidSynth local.
    """
    # 1. On repère les chemins absolus (pour éviter les erreurs)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Chemin vers l'exécutable FluidSynth qu'on vient de coller
    fluidsynth_exe = os.path.join(base_dir, 'fluidsynth', 'bin', 'fluidsynth.exe')
    
    # Chemin vers la SoundFont (le carburant)
    config = load_config()
    # On nettoie le chemin du sf2 (au cas où il y ait des slashs bizarres)
    sf2_rel_path = config['paths']['soundfont']
    soundfont_path = os.path.join(base_dir, sf2_rel_path.replace('/', os.sep))

    print(f"   🎹 Rendu Audio en cours...")
    print(f"      Moteur : {fluidsynth_exe}")
    print(f"      SoundFont : {soundfont_path}")

    # 2. Vérification de sécurité
    if not os.path.exists(fluidsynth_exe):
        raise FileNotFoundError(f"❌ MOTEUR INTROUVABLE : {fluidsynth_exe}")
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"❌ SOUNDFONT INTROUVABLE : {soundfont_path}")

    # 3. La Commande Magique (Subprocess)
    # fluidsynth -ni -g 1.0 -F output.wav soundfont.sf2 input.mid
    cmd = [
        fluidsynth_exe,
        '-ni',              # No Interface (Mode commande)
        '-g', '1.0',        # Gain (Volume)
        '-F', output_wav_path, # Fichier de sortie
        soundfont_path,     # Banque de sons
        midi_path           # Fichier d'entrée
    ]

    # Exécution silencieuse
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   ✨ SUCCÈS ! Audio créé : {output_wav_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ ERREUR MOTEUR : Le rendu a échoué.")
        return False

# --- TEST LOCAL ---
if __name__ == "__main__":
    # Pour tester, on prend le MIDI qu'on a généré à l'étape d'avant
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_midi = os.path.join(base, 'output', 'test_melody.mid')
    test_wav = os.path.join(base, 'output', 'test_audio.wav')
    
    if os.path.exists(test_midi):
        render_wav(test_midi, test_wav)
    else:
        print("⚠️ Lance d'abord composer.py pour avoir un MIDI à tester !")