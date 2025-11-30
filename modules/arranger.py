import music21

def create_full_arrangement(score):
    """
    Assemble le score de base (matière première) en une structure Intro-Couplet-Refrain.
    """
    print("   🏗️ Construction de la structure complète (Arrangement AABA)...")

    # Initialisation du score final
    final_arrangement = music21.stream.Score()
    
    # Récupérer toutes les parties originales du score (Mélodie, Basse, Accords...)
    parts = {p.id: p for p in score.parts}

    # Boucle sur chaque partie (Melody, Bass, Chords, Drums)
    for part_id, original_part in parts.items():
        new_part = music21.stream.Part(id=part_id)
        current_offset = 0.0 # Temps de départ pour l'insertion
        
        # 1. INTRO (4 mesures - Basée sur la Phrase A)
        intro_section = original_part.measures(1, 4)
        new_part.insert(current_offset, intro_section)
        current_offset += 4.0

        # 2. COUPLET 1 (8 mesures - Phrase A répétée 2x)
        couplet_section = original_part.measures(1, 8)
        new_part.insert(current_offset, couplet_section)
        current_offset += 8.0
        
        # 3. REFRAIN / PONT (8 mesures - Phrase B pour le contraste)
        refrain_section = original_part.measures(9, 16)
        new_part.insert(current_offset, refrain_section)
        current_offset += 8.0
        
        # 4. OUTRO / FIN (4 mesures - Basée sur les dernières mesures pour l'atterrissage)
        outro_section = original_part.measures(13, 16) 
        new_part.insert(current_offset, outro_section)
        current_offset += 4.0 # Durée totale du morceau: 24 mesures (4+8+8+4)
        
        final_arrangement.insert(0, new_part) # Ajoute la partie finalisée au score

    print("   ✅ Arrangement final créé (Durée totale : 24 mesures).")
    return final_arrangement