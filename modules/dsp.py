from pedalboard import Pedalboard, Compressor, Gain, Limiter, Reverb
from pedalboard.io import AudioFile
import os

def master_track(input_wav, output_wav):
    """Applique une chaîne de mastering."""
    
    # Définition de la chaîne d'effets
    board = Pedalboard([
        Compressor(threshold_db=-15, ratio=3.0, attack_ms=10, release_ms=400),
        Gain(gain_db=6.0),
        Reverb(room_size=0.25, wet_level=0.1, dry_level=0.9),
        Limiter(threshold_db=-1.0)
    ])

    try:
        # Lecture
        with AudioFile(input_wav) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate

        # Application des effets
        effected_audio = board(audio, samplerate)

        # Sauvegarde
        with AudioFile(output_wav, 'w', samplerate, effected_audio.shape[0]) as f:
            f.write(effected_audio)
            
        return True

    except Exception as e:
        print(f"   ❌ ERREUR DSP : {e}")
        return False