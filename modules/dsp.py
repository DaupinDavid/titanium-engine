from pedalboard import Pedalboard, Compressor, Gain, Limiter, Reverb
from pedalboard.io import AudioFile
import os

def master_track(input_wav, output_wav):
    """
    Applique une chaîne de mastering pro : Compression -> Reverb légère -> Limiter.
    """
    print(f"   🎚️  Mastering en cours...")

    # 1. Définition de la chaîne d'effets (Rack virtuel)
    board = Pedalboard([
        # Compresseur : Écrase les pics pour un son plus dense
        Compressor(threshold_db=-15, ratio=3.0, attack_ms=10, release_ms=400),
        
        # Gain : On monte le volume (Make-up gain)
        Gain(gain_db=6.0),
        
        # Reverb : Un tout petit peu d'espace (pour ne pas que ça sonne 'sec')
        Reverb(room_size=0.25, wet_level=0.1, dry_level=0.9),

        # Limiter : Le plafond de verre à -1dB pour ne jamais saturer
        Limiter(threshold_db=-1.0)
    ])

    # 2. Traitement du fichier audio
    try:
        # Lecture
        with AudioFile(input_wav) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate

        # Application des effets (C'est ici que la magie opère)
        effected_audio = board(audio, samplerate)

        # Sauvegarde
        with AudioFile(output_wav, 'w', samplerate, effected_audio.shape[0]) as f:
            f.write(effected_audio)
            
        print(f"   ✨ Mastering terminé : {output_wav}")
        return True

    except Exception as e:
        print(f"   ❌ ERREUR DSP : {e}")
        return False

# --- TEST LOCAL ---
if __name__ == "__main__":
    # On reprend le fichier brut généré juste avant
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_wav = os.path.join(base, 'output', 'test_audio.wav')
    mastered_wav = os.path.join(base, 'output', 'test_audio_mastered.wav')
    
    if os.path.exists(raw_wav):
        master_track(raw_wav, mastered_wav)
    else:
        print("⚠️ Lance d'abord synthesizer.py pour avoir un son à masteriser !")