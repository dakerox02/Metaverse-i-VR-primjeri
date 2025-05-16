import cv2
import numpy as np

image = cv2.imread(r"C:\Users\PC\Documents\simulacija\panorama.jpg")
if image is None:
    raise ValueError("Slika nije pronađena. Provjeri da li je putanja tačna.")

# Ovdje postavljamo dimenzije za ekran
screen_width = 1920
screen_height = 1020

# Ovdje smo zbog ogranicenja stavili da bi se fino na ekrana napravilo
scale_x = screen_width / image.shape[1]
scale_y = screen_height / image.shape[0]
scale = min(scale_x, scale_y)

new_width = int(image.shape[1] * scale)
new_height = int(image.shape[0] * scale)

# Ovdje smo skalirali sliku
image = cv2.resize(image, (new_width, new_height))

height, width, _ = image.shape

# Postavljamo viewport odnosno dio kroz koji ce slika biti izostrena
viewport_width = int(300 * scale)
viewport_height = int(300 * scale)

# Početna pozicija viewporta
x_pos = 0
y_pos = height // 2 - viewport_height // 2

#Pravimo sum na slici odnosno blurujemo
blurred_image = cv2.GaussianBlur(image, (31, 31), 0)

def apply_viewport_blending(x, y):
    blended = blurred_image.copy()
    
    # Granice viewporta da ne bi ispali iz slike
    x1 = min(max(0, x), width - viewport_width)
    x2 = x1 + viewport_width
    y1 = min(max(0, y), height - viewport_height)
    y2 = y1 + viewport_height

    # Ubacujemo oštar dio slike unutar viewporta
    blended[y1:y2, x1:x2] = image[y1:y2, x1:x2]
    
    # Okvir viewporta
    cv2.rectangle(blended, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return blended

# Uputstvo
print("Koristi W/A/S/D za pomjeranje viewporta. ESC za izlaz.")

# Glavna petlja
while True:
    frame = apply_viewport_blending(x_pos, y_pos)
    cv2.imshow("VR Tile-based Viewport Simulation", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('a') or key == ord('A'):  # Lijevo
        x_pos = max(0, x_pos - 20)
    elif key == ord('d') or key == ord('D'):  # Desno
        x_pos = min(width - viewport_width, x_pos + 20)
    elif key == ord('w') or key == ord('W'):  # Gore
        y_pos = max(0, y_pos - 20)
    elif key == ord('s') or key == ord('S'):  # Dolje
        y_pos = min(height - viewport_height, y_pos + 20)

cv2.destroyAllWindows()
