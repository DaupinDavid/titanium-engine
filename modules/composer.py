import music21
import random
import json
import os
from datetime import datetime

def load_config():
    """Charge la configuration depuis le fichier JSON à la racine."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_melody(duration_measures=16):
    """
    Génère les pistes Melodie, Accords, Basse, et Drums avec la structure et le voicing.
    """
    config = load_config()
    settings = config['generation_settings']
    instruments_config = settings['instruments']
    
    # 1. PARAMÈTRES DE BASE
    bpm = random.randint(settings['bpm_range'][0], settings['bpm_range'][1])
    key_str = settings['default_key'] 
    
    score = music21.stream.Score()
    score.insert(0, music21.tempo.MetronomeMark(number=bpm))
    my_key = music21.key.Key(key_str.split()[0], key_str.split()[1].lower())
    
    scale = my_key.getScale()
    pitches = scale.getPitches('C4', 'C5') 
    
    # Structure Harmonique Fonctionnelle (I-vi-IV-V)
    tonic = my_key.tonic
    submediant = tonic.transpose(9) 
    subdominant = tonic.transpose(5) 
    dominant = tonic.transpose(7) 
    progression_roots = [tonic, submediant, subdominant, dominant] * 4 # 16 mesures
    
    # --- CRÉATION DES PARTIES ---
    part_melody = music21.stream.Part(id='Melody')
    part_chords = music21.stream.Part(id='Chords')
    part_bass = music21.stream.Part(id='Bass')
    part_drums = music21.stream.Part(id='Drums')
    
    # ASSIGNATION DES INSTRUMENTS
    inst_melody = music21.instrument.Piano() 
    inst_melody.midiProgram = instruments_config['melody_midi_program'] 
    part_melody.insert(0, inst_melody)
    
    inst_bass = music21.instrument.ElectricBass()
    inst_bass.midiProgram = instruments_config['bass_midi_program']
    part_bass.insert(0, inst_bass)
    
    inst_chords = music21.instrument.Instrument() 
    inst_chords.midiProgram = 90
    part_chords.insert(0, inst_chords)
    
    part_drums.insert(0, music21.instrument.Percussion())

    # Variables de contrôle
    current_pitch = random.choice(pitches)
    
    # --- FIX NAME ERROR ET RYTHME FINAL ---
    possible_rhythms = [1.0, 0.5, 0.25, 1.5]
    rhythmic_motif = [0.75, 0.25, 1.0, 1.0] # Le motif utilisé par la mélodie
    # -------------------------------------
    
    # 4. REMPLISSAGE DES 16 MESURES
    for measure_index, root in enumerate(progression_roots):
        
        # A. ACCORDS & BASSE
        chord_root = root.transpose(12) 
        c = music21.chord.Chord([chord_root, chord_root.transpose(4), chord_root.transpose(7)])
        c.quarterLength = 4.0 
        part_chords.append(c)

        b = music21.note.Note(root)
        b.octave = 2 
        b.quarterLength = 4.0
        part_bass.append(b)
        
        chord_notes_str = [c.notes[0].nameWithOctave, c.notes[1].nameWithOctave, c.notes[2].nameWithOctave]

        # B. BATTERIE (Pattern Syncopé - Le son qui donne le groove)
        part_drums.append(music21.note.Note(36, quarterLength=0.5, volume=music21.volume.Volume(velocity=90))) 
        part_drums.append(music21.note.Rest(quarterLength=0.5)) 
        part_drums.append(music21.note.Note(38, quarterLength=1.0, volume=music21.volume.Volume(velocity=100)))
        part_drums.append(music21.note.Note(36, quarterLength=0.5, volume=music21.volume.Volume(velocity=80))) 
        part_drums.append(music21.note.Note(42, quarterLength=0.5, volume=music21.volume.Volume(velocity=60))) 
        part_drums.append(music21.note.Note(42, quarterLength=1.0, volume=music21.volume.Volume(velocity=60)))


        # C. MELODIE (Marche intelligente avec direction et résolution)
        current_measure_time = 0.0
        rhythm_index = 0
        
        while current_measure_time < 4.0:
            # Utilise un rythme simple pour cette version pour éviter les erreurs de dépassement
            q_length = random.choice([1.0, 0.5]) 
            
            if current_measure_time == 4.0 - q_length:
                final_pitch_str = random.choice(chord_notes_str)
                new_pitch = music21.pitch.Pitch(final_pitch_str)
            else:
                if random.random() < 0.9:
                    step = random.choice([-1, 0, 1])
                else:
                    step = random.choice([-3, 3])
                try:
                    new_pitch = current_pitch.transpose(step)
                except:
                    new_pitch = current_pitch

                if new_pitch not in pitches:
                    new_pitch = current_pitch

            if random.random() < 0.05: 
                part_melody.append(music21.note.Rest(quarterLength=q_length))
            else:
                part_melody.append(music21.note.Note(new_pitch, quarterLength=q_length))
                current_pitch = new_pitch 
                
            current_measure_time += q_length

    # 5. ASSEMBLAGE FINAL
    score.append(part_chords)
    score.append(part_bass)
    score.append(part_drums)
    score.append(part_melody) 
    return score, bpm