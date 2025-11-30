from pedalboard import Pedalboard, Compressor, Gain, Limiter, Reverb, Distortion, Delay
from pedalboard.io import AudioFile
import os
import numpy as np

def master_track(main_wav_path, texture_wav_path, output_wav_path):
    """
    Charge la piste principale et la texture, les mélange, applique les effets, et sauvegarde.
    """
    print(f"   🎚️  Mixage et Mastering en cours...")

    try:
        # 1. Lecture de la piste principale (FluidSynth)
        with AudioFile(main_wav_path) as f_main:
            main_audio = f_main.read(f_main.frames)
            samplerate = f_main.samplerate
        
        # 2. Lecture de la texture (Bruit de fond)
        with AudioFile(texture_wav_path) as f_texture:
            texture_audio = f_texture.read(f_texture.frames)

        # 3. Harmonisation des longueurs (Couper ce qui dépasse)
        min_length = min(main_audio.shape[1], texture_audio.shape[1])
        main_audio = main_audio[:, :min_length]
        texture_audio = texture_audio[:, :min_length]

        # 4. LE MIXAGE : On ajoute la texture à 25% du volume
        # (Attention aux dimensions des arrays numpy)
        mixed_audio = main_audio + (texture_audio * 0.25)

        # 5. CHAÎNE D'EFFETS (CORRIGÉE)
        board = Pedalboard([
            # Chaleur analogique (Remplace Overdrive qui buggait)
            Distortion(drive_db=6.0), 
            
            # Compression pour lier la texture et l'instru
            Compressor(threshold_db=-18, ratio=3.0, attack_ms=10, release_ms=400),
            
            # Espace stéréo (Argument 'delay_seconds' corrigé)
            Delay(delay_seconds=0.08, feedback=0.2, mix=0.15), 
            
            # Ambiance globale
            Reverb(room_size=0.35, wet_level=0.1, dry_level=0.9),

            # Protection finale
            Limiter(threshold_db=-1.0),
            
            # Volume final
            Gain(gain_db=3.0)
        ])

        # 6. Application des effets
        effected_audio = board(mixed_audio, samplerate)

        # 7. Sauvegarde finale
        with AudioFile(output_wav_path, 'w', samplerate, effected_audio.shape[0]) as f:
            f.write(effected_audio)
            
        print(f"   ✨ Mixage Texture + Mastering terminé.")
        return True

    except Exception as e:
        print(f"   ❌ ERREUR DSP (Mixage) : {e}")
        # En cas d'erreur de mixage, on essaie de sauver juste le raw pour ne pas tout perdre
        # shutil.copy(main_wav_path, output_wav_path) 
        return False