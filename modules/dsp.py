from pedalboard import Pedalboard, Compressor, Gain, Limiter, Reverb, Distortion, Delay
from pedalboard.io import AudioFile
import numpy as np

def master_track(main_wav, texture_wav, out_wav):
    print("   🎚️ Mixage & Mastering...")
    try:
        with AudioFile(main_wav) as f:
            audio = f.read(f.frames)
            sr = f.samplerate
            
        with AudioFile(texture_wav) as f:
            # On boucle la texture si elle est trop courte, ou on la coupe
            tex = f.read(f.frames)
            
        # Ajustement longueur (bourrin mais efficace)
        len_main = audio.shape[1]
        len_tex = tex.shape[1]
        
        if len_tex < len_main:
            # Si texture trop courte, on pad avec des 0
            tex = np.pad(tex, ((0,0), (0, len_main - len_tex)))
        else:
            tex = tex[:, :len_main]

        # MIXAGE (Instru 100% + Texture 20%)
        mixed = audio + (tex * 0.2)

        # EFFETS
        board = Pedalboard([
            Distortion(drive_db=2.0), # Un peu de chaleur
            Compressor(threshold_db=-16, ratio=2.5),
            Reverb(room_size=0.4, wet_level=0.15),
            Limiter(threshold_db=-0.5),
            Gain(gain_db=3.0)
        ])
        
        rendered = board(mixed, sr)

        with AudioFile(out_wav, 'w', sr, rendered.shape[0]) as f:
            f.write(rendered)
            
        return True
    except Exception as e:
        print(f"   ❌ ERREUR DSP: {e}")
        return False