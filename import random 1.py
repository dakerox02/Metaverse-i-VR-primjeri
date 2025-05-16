import random
import time

# Simulacija 360° podijeljene na blokove
scene_blocks = [i for i in range(0, 360, 30)]  # Na svakih 30 stepeni jedan blok (12 blokova)

def simulate_user_gaze():
    """Simulira nasumičan ugao gdje korisnik trenutno gleda."""
    return random.choice(scene_blocks)

def stream_block(block_angle, user_gaze):
    """Odlučuje da li blok strimovati u visokoj ili niskoj rezoluciji."""
    # Ako je blok unutar ±30 stepeni od pogleda, strimujemo visoki kvalitet
    if abs(block_angle - user_gaze) <= 30 or abs(block_angle - user_gaze) >= 330:
        return f"Block {block_angle}° -> HIGH quality"
    else:
        return f"Block {block_angle}° -> LOW quality"

def simulate_streaming():
    for _ in range(5):
        user_gaze = simulate_user_gaze()
        print(f"\n[User gaze at {user_gaze}°]:")
        
        for block in scene_blocks:
            decision = stream_block(block, user_gaze)
            print(decision)
        
        time.sleep(2) 

simulate_streaming()
