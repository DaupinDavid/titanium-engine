import music21
import random
import json
import os

def load_config():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    with open(config_path, 'r') as f: return json.load(f)

def generate_melody(duration_measures=16):
    config = load_config()
    settings = config['generation_settings']
    instruments = settings['instruments']
    
    bpm = random.randint(settings['bpm_range'][0], settings['bpm_range'][1])
    key_str = settings['default_key'] 
    
    score = music21.stream.Score()
    score.insert(0, music21.tempo.MetronomeMark(number=bpm))
    my_key = music21.key.Key(key_str.split()[0], key_str.split()[1].lower())
    
    scale = my_key.getScale()
    pitches = scale.getPitches('C4', 'C5') 
    
    # Progression AABA (I-vi-IV-V)
    roots = [my_key.tonic, my_key.tonic.transpose(9), my_key.tonic.transpose(5), my_key.tonic.transpose(7)] * 4
    
    # PARTIES
    p_melody = music21.stream.Part(id='Melody')
    p_chords = music21.stream.Part(id='Chords')
    p_bass = music21.stream.Part(id='Bass')
    p_drums = music21.stream.Part(id='Drums')
    
    # INSTRUMENTS
    p_melody.insert(0, music21.instrument.Piano())
    p_bass.insert(0, music21.instrument.ElectricBass())
    p_chords.insert(0, music21.instrument.StringInstrument()) # Nappe cordes
    p_drums.insert(0, music21.instrument.Percussion())

    curr_pitch = random.choice(pitches)
    
    for i, root in enumerate(roots):
        # 1. ACCORDS
        c = music21.chord.Chord([root.transpose(12), root.transpose(16), root.transpose(19)])
        c.quarterLength = 4.0
        p_chords.append(c)

        # 2. BASSE
        p_bass.append(music21.note.Note(root, quarterLength=4.0, octave=2))

        # 3. DRUMS (Kick/Snare simple et efficace)
        p_drums.append(music21.note.Note(36, quarterLength=1.0, volume=90)) # Kick
        p_drums.append(music21.note.Note(38, quarterLength=1.0, volume=100)) # Snare
        p_drums.append(music21.note.Note(36, quarterLength=1.0, volume=90)) # Kick
        p_drums.append(music21.note.Note(38, quarterLength=1.0, volume=100)) # Snare

        # 4. MELODIE
        time_left = 4.0
        while time_left > 0:
            dur = random.choice([0.5, 1.0])
            if dur > time_left: dur = time_left
            
            # Résolution sur la fin
            if time_left == dur:
                note_val = music21.note.Note(root.transpose(24), quarterLength=dur)
            else:
                step = random.choice([-2, -1, 0, 1, 2])
                try: curr_pitch = curr_pitch.transpose(step)
                except: pass
                if curr_pitch not in pitches: curr_pitch = pitches[0]
                note_val = music21.note.Note(curr_pitch, quarterLength=dur)
            
            p_melody.append(note_val)
            time_left -= dur

    score.append(p_chords)
    score.append(p_bass)
    score.append(p_drums)
    score.append(p_melody)
    return score, bpm