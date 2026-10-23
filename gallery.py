import cv2
import os
from datetime import datetime

FOLDER = "drawings"

images = [f for f in os.listdir(FOLDER) if f.endswith(".png")]

if not images:
    print("No drawings found!")
    exit()

index = 0

def get_creation_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y  %H:%M:%S")

def show_image():
    global index
    img_path = os.path.join(FOLDER, images[index])
    img = cv2.imread(img_path)

    img = cv2.resize(img, (900, 500))
    h, w, _ = img.shape

    # Get creation date
    created_date = get_creation_date(img_path)

    # Top bar
    cv2.rectangle(img, (0, 0), (w, 40), (40, 40, 40), -1)
    cv2.putText(img, "AIR CANVAS GALLERY", (20, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Bottom bar
    cv2.rectangle(img, (0, h - 80), (w, h), (40, 40, 40), -1)

    info_text = f"Image {index+1} / {len(images)}"
    file_text = f"File: {images[index]}"
    date_text = f"Created: {created_date}"
    controls_text = "Prev: A | Next: D | Delete: X | Exit: Q"

    cv2.putText(img, info_text, (20, h - 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, file_text, (20, h - 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.putText(img, date_text, (20, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

    cv2.putText(img, controls_text, (420, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    cv2.imshow("Gallery", img)

show_image()

while True:
    key = cv2.waitKey(0)

    # NEXT IMAGE (Right Arrow or D)
    if key in [ord('d'), 2555904, 83]:
        index = (index + 1) % len(images)
        show_image()

    # PREVIOUS IMAGE (Left Arrow or A)
    elif key in [ord('a'), 2424832, 81]:
        index = (index - 1) % len(images)
        show_image()

    # DELETE IMAGE (X)
    elif key == ord('x'):
        img_path = os.path.join(FOLDER, images[index])
        os.remove(img_path)
        print("Deleted:", images[index])
        images.pop(index)

        if not images:
            print("No images left!")
            break

        index = index % len(images)
        show_image()

    # EXIT (Q or ESC)
    elif key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
