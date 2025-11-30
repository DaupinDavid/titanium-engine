import music21
import random

def humanize_score(score):
    """
    Modifie un score music21 pour ajouter des nuances humaines (timing et vélocité).
    """
    print("   🤖 Humanisation du score en cours...")

    # Paramètres de chaos contrôlé
    MAX_VELOCITY_SHIFT = 15 
    MAX_OFFSET_SHIFT = 0.03 

    for part in score.parts:
        if part.id == 'Melody' or part.id == 'Chords' or part.id == 'Bass':
            for element in part.flat.notes:
                
                # 1. Humanisation de la Vélocité (Force de frappe)
                if element.volume.velocity is not None:
                    shift = random.randint(-MAX_VELOCITY_SHIFT, MAX_VELOCITY_SHIFT)
                    new_velocity = max(0, min(127, element.volume.velocity + shift))
                    element.volume.velocity = new_velocity
                
                # 2. Humanisation du Timing (Chaos subtil)
                if element.offset is not None:
                    offset_shift = random.uniform(-MAX_OFFSET_SHIFT, MAX_OFFSET_SHIFT)
                    element.offset += offset_shift

    print("   ✅ Nuances humaines appliquées.")
    return score