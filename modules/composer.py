import music21
import random
import json
import os

def load_config():
    """Charge la configuration depuis le fichier JSON à la racine."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_melody(duration_measures=8):
    """
    Génère une mélodie monophonique simple.
    Retourne un objet Score music21 et le BPM choisi.
    """
    config = load_config()
    settings = config['generation_settings']
    
    # 1. Paramètres de base
    bpm = random.randint(settings['bpm_range'][0], settings['bpm_range'][1])
    key_str = settings['default_key'] 
    print(f"   🎲 Composition en cours : {key_str} à {bpm} BPM...")

    # 2. Création de la structure Music21
    score = music21.stream.Score()
    part_melody = music21.stream.Part()
    part_melody.id = 'Melody'
    
    # Ajout du Tempo et de la Tonalité
    part_melody.append(music21.tempo.MetronomeMark(number=bpm))
    my_key = music21.key.Key(key_str.split()[0], key_str.split()[1].lower())
    part_melody.append(my_key)

    # 3. La Gamme (Le terrain de jeu)
    scale = my_key.getScale()
    pitches = scale.getPitches('C4', 'C6') # Notes autorisées
    
    # 4. Génération (Marche Aléatoire)
    for measure in range(duration_measures):
        for beat in range(4): 
            if random.random() < 0.2: # Silence
                r = music21.note.Rest()
                r.quarterLength = 1.0
                part_melody.append(r)
            else: # Note
                note_pitch = random.choice(pitches)
                n = music21.note.Note(note_pitch)
                n.quarterLength = 1.0
                part_melody.append(n)

    score.append(part_melody)
    return score, bpm

# --- TEST LOCAL ---
if __name__ == "__main__":
    print("🧪 Test du module COMPOSER...")
    try:
        s, b = generate_melody()
        # Chemin de sortie pour le test
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        test_path = os.path.join(output_dir, 'test_melody.mid')
        s.write('midi', fp=test_path)
        print(f"✅ SUCCÈS ! Fichier MIDI généré : {test_path}")
    except Exception as e:
        print(f"❌ ERREUR : {e}")