import os
import subprocess
import json
import sys

def load_config():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(1)

def render_wav(midi_path, soundfont_path, output_wav_path):
    """
    Version NUCLÉAIRE pour Windows : Injection de PATH et Chemins Absolus.
    """
    # 1. Chemins Absolus (Pas d'ambiguïté)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    midi_abs = os.path.abspath(midi_path)
    sf2_abs = os.path.abspath(soundfont_path)
    out_abs = os.path.abspath(output_wav_path)

    # 2. Configuration du Moteur
    if os.name == 'nt':
        fluidsynth_dir = os.path.join(base_dir, 'fluidsynth', 'bin')
        executable = os.path.join(fluidsynth_dir, 'fluidsynth.exe')
        
        # --- INJECTION DE DLL (CRITIQUE) ---
        # On dit à Windows : "Cherche les DLLs ici aussi !"
        my_env = os.environ.copy()
        my_env["PATH"] = fluidsynth_dir + os.pathsep + my_env["PATH"]
    else:
        executable = 'fluidsynth'
        my_env = os.environ.copy()

    # 3. Vérifications
    if not os.path.exists(sf2_abs):
        print(f"❌ ERREUR : Soundfont introuvable : {sf2_abs}")
        return False
    
    # 4. Commande (Syntaxe stricte FluidSynth 2.5)
    # Exe | Soundfont | MIDI | Options | Sortie
    cmd = [
        executable,
        '-ni',              # No Interface
        sf2_abs,            # SoundFont (Absolu)
        midi_abs,           # MIDI (Absolu)
        '-F', out_abs,      # Sortie (Absolue)
        '-r', '44100',      # Force Sample Rate
        '-g', '1.0'         # Gain
    ]

    # 5. EXÉCUTION
    print(f"   🔍 Exécution Moteur...")
    try:
        # On capture TOUT pour voir pourquoi ça plante
        result = subprocess.run(
            cmd, 
            env=my_env,       # <-- C'est ici que l'injection agit
            check=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ CRASH MOTEUR (Code {e.returncode}) :")
        print(f"--- LOG DU MOTEUR ---")
        print(e.stdout)
        print(e.stderr)
        print(f"---------------------")
        return False
    except OSError as e:
        print(f"\n❌ ERREUR SYSTÈME (WinError 193 probable) : {e}")
        return False