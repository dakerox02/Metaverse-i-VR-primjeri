import cv2
import numpy as np

video_path = r"C:\Users\PC\Documents\VRsimulacija\video360.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise ValueError("Video nije pronađen.")

ret, frame = cap.read()
if not ret:
    raise ValueError("Ne može se učitati prvi frejm.")

# Vrsimo skaliranje kao i kod slike sto smo radili
screen_width = 1280
screen_height = 720
scale = min(screen_width / frame.shape[1], screen_height / frame.shape[0])
new_width = int(frame.shape[1] * scale)
new_height = int(frame.shape[0] * scale)


circle_radius = int(60 * scale)
circle_distance = int(120 * scale)  # razmak između centara krugova

#Početna pozicija
x_center = new_width // 2
y_center = new_height // 2

# Korisničko uputstvo
print("Pokrenuto. WASD za pomjeranje ∞ viewporta. ESC za izlaz.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (new_width, new_height))
    blurred = cv2.GaussianBlur(frame, (35, 35), 0)

    # Maska za dva kruga (∞)
    mask = np.zeros((new_height, new_width), dtype=np.uint8)
    left_center = (x_center - circle_distance // 2, y_center)
    right_center = (x_center + circle_distance // 2, y_center)

    cv2.circle(mask, left_center, circle_radius, 255, -1)
    cv2.circle(mask, right_center, circle_radius, 255, -1)

    # Primijeninjujemo masku (gdje je maska bijela, prikazujemo oštru sliku)
    mask_3ch = cv2.merge([mask, mask, mask])
    result = np.where(mask_3ch == 255, frame, blurred)


    cv2.circle(result, left_center, circle_radius, (0, 255, 0), 2)
    cv2.circle(result, right_center, circle_radius, (0, 255, 0), 2)

    # Prikaz
    cv2.imshow("∞ VR Viewport Simulacija", result)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('a') or key == ord('A'):  # lijevo
        x_center = max(circle_distance // 2 + circle_radius, x_center - 20)
    elif key == ord('d') or key == ord('D'):  # desno
        x_center = min(new_width - circle_distance // 2 - circle_radius, x_center + 20)
    elif key == ord('w') or key == ord('W'):  # gore
        y_center = max(circle_radius, y_center - 20)
    elif key == ord('s') or key == ord('S'):  # dolje
        y_center = min(new_height - circle_radius, y_center + 20)

cap.release()
cv2.destroyAllWindows()
