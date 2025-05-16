import random
import time

# Simulacija 360° podijeljene na blokove
scene_blocks = [i for i in range(0, 360, 30)]  # Na svakih 30 stepeni jedan blok (12 blokova)

def simulate_user_gaze(current_gaze=None):
    """Simulira korisnički pogled - može malo da se pomjeri od trenutnog."""
    if current_gaze is None:
        return random.choice(scene_blocks)
    move = random.choice([-30, 0, 30])  # Korisnik može da ostane, okrene lijevo ili desno za 30 stepeni
    new_gaze = (current_gaze + move) % 360
    return new_gaze

def predict_next_gaze(current_gaze):
    """Predviđa gdje će korisnik sljedeće gledati (najverovatnije ista ili bliska pozicija)."""
    prediction = (current_gaze + random.choice([0, 30])) % 360
    return prediction

def stream_block(block_angle, user_gaze, predicted_gaze):
    """Odlučuje da li blok strimovati u visokom ili niskom kvalitetu."""
    # Ako je blok u vidnom polju ili blizu predikcije
    if (abs(block_angle - user_gaze) <= 30 or abs(block_angle - user_gaze) >= 330 or
        abs(block_angle - predicted_gaze) <= 30 or abs(block_angle - predicted_gaze) >= 330):
        return "H"  # High quality
    else:
        return "L"  # Low quality

def visualize_stream(scene_status):
    """Prikazuje status svih blokova kao ASCII kružnicu."""
    print("\n360° Scene status:")
    visual = ""
    for angle, quality in scene_status.items():
        visual += f"|{quality}{angle}°"
    visual += "|"
    print(visual)
    print()

def simulate_streaming():
    current_gaze = None
    for cycle in range(5):  
        current_gaze = simulate_user_gaze(current_gaze)
        predicted_gaze = predict_next_gaze(current_gaze)

        print(f"Cycle {cycle+1}:")
        print(f"User gaze: {current_gaze}° | Predicted next gaze: {predicted_gaze}°")

        scene_status = {}
        for block in scene_blocks:
            quality = stream_block(block, current_gaze, predicted_gaze)
            scene_status[block] = quality
        
        visualize_stream(scene_status)
        time.sleep(2)


simulate_streaming()
