import os
import subprocess
import shutil
import sys

def render_wav(midi_path, soundfont_path, output_wav_path):
    """
    EXÉCUTION EN ZONE SÛRE (C:\SF2).
    Contourne tous les bugs d'espaces et de chemins Windows.
    """
    # 1. ZONE DE TRAVAIL (Doit exister)
    work_dir = "C:\\SF2"
    if not os.path.exists(work_dir):
        print(f"❌ ERREUR: Le dossier {work_dir} n'existe pas. Créez-le et mettez le SF2 dedans.")
        return False

    # Noms de fichiers temporaires simples
    temp_midi = os.path.join(work_dir, "temp.mid")
    temp_wav = os.path.join(work_dir, "temp.wav")
    
    # 2. NETTOYAGE & COPIE DU MIDI
    if os.path.exists(temp_wav): os.remove(temp_wav)
    try:
        shutil.copy(midi_path, temp_midi)
    except Exception as e:
        print(f"❌ ERREUR COPIE MIDI: {e}")
        return False

    # 3. RECHERCHE DE L'EXECUTABLE
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fluidsynth_exe = os.path.join(base_dir, 'fluidsynth', 'bin', 'fluidsynth.exe')
    
    if not os.path.exists(fluidsynth_exe):
        print(f"❌ ERREUR EXE: Introuvable à {fluidsynth_exe}")
        return False

    # 4. COMMANDE SIMPLE (Tout est dans C:\SF2)
    # soundfont.sf2 doit être dans C:\SF2
    sf2_name = "soundfont.sf2" 
    
    cmd = [
        fluidsynth_exe,
        '-ni',
        '-g', '1.5', # Gain boosté
        sf2_name,    # Juste le nom, car on sera dans le dossier
        "temp.mid",
        '-F', "temp.wav"
    ]

    print(f"   🔥 EXÉCUTION FLUIDSYNTH DANS {work_dir}...")
    
    try:
        # ON CHANGE LE DOSSIER D'EXÉCUTION (CWD)
        result = subprocess.run(
            cmd,
            cwd=work_dir, # <-- MAGIE ICI
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 5. RAPATRIEMENT
        if os.path.exists(temp_wav) and os.path.getsize(temp_wav) > 50000: # Doit être > 50ko
            if os.path.exists(output_wav_path): os.remove(output_wav_path)
            shutil.move(temp_wav, output_wav_path)
            print(f"   ✅ SUCCÈS : Audio généré et rapatrié.")
            return True
        else:
            print(f"   ❌ ÉCHEC : Fichier audio vide ou absent.")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"   ❌ CRASH SYSTÈME : {e}")
        return False