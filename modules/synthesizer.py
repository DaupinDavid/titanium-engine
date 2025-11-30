import os
import subprocess
import shutil
import sys

def render_wav(midi_path, soundfont_path, output_wav_path):
    """
    MOTEUR HYBRIDE :
    - Sur WINDOWS : Utilise la zone tampon C:\SF2 (Anti-bug espaces).
    - Sur LINUX (Cloud) : Utilise les chemins standards (Rapide).
    """
    
    # --- CAS 1 : WINDOWS (Mode "Nucléaire" C:\SF2) ---
    if os.name == 'nt':
        work_dir = r"C:\SF2"
        if not os.path.exists(work_dir):
            # Si le dossier n'existe pas, on tente de le créer, sinon erreur
            try:
                os.makedirs(work_dir)
            except:
                print(f"❌ ERREUR: Impossible de créer {work_dir}")
                return False

        temp_midi = os.path.join(work_dir, "temp.mid")
        temp_wav = os.path.join(work_dir, "temp.wav")
        sf2_name = "soundfont.sf2" # On suppose qu'il est déjà là-bas
        
        # Copie MIDI
        try:
            shutil.copy(midi_path, temp_midi)
        except Exception as e:
            print(f"❌ ERREUR COPIE MIDI: {e}")
            return False

        # Recherche EXE
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fluidsynth_exe = os.path.join(base_dir, 'fluidsynth', 'bin', 'fluidsynth.exe')

        cmd = [
            fluidsynth_exe,
            '-ni',
            '-g', '1.5',
            '-F', temp_wav,
            sf2_name,
            "temp.mid"
        ]
        
        cwd_path = work_dir

    # --- CAS 2 : LINUX / CLOUD (Mode Standard Propre) ---
    else:
        # Sur Render, le SoundFont est dans /app/assets/... pas dans C:\SF2
        # On utilise les chemins réels fournis par le code
        cmd = [
            'fluidsynth', # Installé globalement via Docker
            '-ni',
            '-g', '1.5',
            '-F', output_wav_path, # On écrit directement au bon endroit
            soundfont_path,
            midi_path
        ]
        cwd_path = None # Pas besoin de changer de dossier

    # --- EXÉCUTION COMMUNE ---
    print(f"   🔥 EXÉCUTION FLUIDSYNTH (Mode {'Windows' if os.name == 'nt' else 'Linux'})...")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # GESTION DES RÉSULTATS
        if os.name == 'nt':
            # Rapatriement Windows
            if os.path.exists(temp_wav) and os.path.getsize(temp_wav) > 50000:
                if os.path.exists(output_wav_path): os.remove(output_wav_path)
                shutil.move(temp_wav, output_wav_path)
                return True
            else:
                print(f"   ❌ ÉCHEC : {result.stderr}")
                return False
        else:
            # Vérification Linux
            if os.path.exists(output_wav_path) and os.path.getsize(output_wav_path) > 50000:
                return True
            else:
                print(f"   ❌ ÉCHEC LINUX : {result.stderr}")
                return False

    except Exception as e:
        print(f"   ❌ CRASH SYSTÈME : {e}")
        return False