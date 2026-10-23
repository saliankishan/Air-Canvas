
import cv2
import mediapipe as mp
import numpy as np
import time
import os
from datetime import datetime
from utils.hand_utils import fingers_up

from database import init_db, save_drawing

# ----------------------------
# INIT DATABASE & FOLDERS
# ----------------------------
init_db()
if not os.path.exists("drawings"):
    os.mkdir("drawings")

# ----------------------------
# CAMERA SETUP (SMALL + FAST)
# ----------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

cv2.namedWindow("Air Canvas", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Air Canvas", 1000, 600)

# ----------------------------
# MEDIAPIPE SETUP
# ----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ----------------------------
# CANVAS & COLORS
# ----------------------------
canvas = None
prev_x, prev_y = 0, 0
last_save_time = 0

undo_stack = []
MAX_UNDO = 10

colors = [
    (255, 0, 255),   # Purple
    (255, 0, 0),     # Blue
    (0, 255, 0),     # Green
    (0, 255, 255),   # Yellow
    (0, 0, 0)        # Eraser
]
color_names = ["PURPLE", "BLUE", "GREEN", "YELLOW", "ERASER"]
current_color = colors[0]
current_color_name = color_names[0]

# ----------------------------
# DRAW TOP TOOLBAR
# ----------------------------
def draw_toolbar(img):
    h, w, _ = img.shape
    cv2.rectangle(img, (0, 0), (w, 50), (40, 40, 40), -1)
    cv2.putText(img, "AIR CANVAS", (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    box_w = 70
    for i, col in enumerate(colors):
        x1 = 200 + i * box_w
        x2 = x1 + box_w
        cv2.rectangle(img, (x1, 10), (x2, 40), col, -1)

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Toolbar
    draw_toolbar(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    mode = "NONE"

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            thumb, index, middle, ring, pinky = fingers_up(hand)

            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            # 🎨 SELECT COLOR
            if index and middle:
                mode = "SELECT"
                prev_x, prev_y = 0, 0
                if y < 50:
                    box_w = 70
                    idx = (x - 200) // box_w
                    if 0 <= idx < len(colors):
                        current_color = colors[idx]
                        current_color_name = color_names[idx]

            # ✏️ DRAW
            elif index and not middle:
                mode = "DRAW"

                if len(undo_stack) == 0 or len(undo_stack) < MAX_UNDO:
                    undo_stack.append(canvas.copy())

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                thickness = 30 if current_color == (0, 0, 0) else 6
                cv2.line(canvas, (prev_x, prev_y), (x, y),
                         current_color, thickness)
                prev_x, prev_y = x, y

            # 💾 SAVE
            elif thumb and not index:
                mode = "SAVE"
                if time.time() - last_save_time > 2:
                    filename = f"drawings/img_{int(time.time())}.png"
                    cv2.imwrite(filename, canvas)
                    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_drawing(filename, current_color_name, mode, time_str)
                    last_save_time = time.time()

            else:
                prev_x, prev_y = 0, 0

    # MERGE CANVAS
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    # ----------------------------
    # RIGHT STATUS PANEL (SMALL)
    # ----------------------------
    panel_w = 180
    px1 = w - panel_w
    cv2.rectangle(frame, (px1, 70), (w, h - 30), (60, 60, 60), -1)

    status_text = [
        "STATUS",
        f"Mode: {mode}",
        f"Color: {current_color_name}",
        "C : Clear",
        "Ctrl+Z : Undo",
        "Q : Quit"
    ]

    for i, txt in enumerate(status_text):
        cv2.putText(frame, txt, (px1 + 10, 100 + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # ----------------------------
    # BOTTOM STATUS BAR
    # ----------------------------
    cv2.rectangle(frame, (0, h - 25), (w, h), (40, 40, 40), -1)
    cv2.putText(frame,
                "Draw: Index | Color: Index+Middle | Save: Thumb | C: Clear | Ctrl+Z: Undo",
                (10, h - 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    # ----------------------------
    # KEYBOARD CONTROLS
    # ----------------------------
    key = cv2.waitKey(1) & 0xFF

    # C = Clear
    if key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        mode = "CLEAR"

    # Ctrl + Z = Undo
    if key == 26 and undo_stack:
        canvas = undo_stack.pop()
        mode = "UNDO"

    # Q = Quit
    if key == ord('q'):
        break

    cv2.imshow("Air Canvas", frame)

cap.release()
cv2.destroyAllWindows()
