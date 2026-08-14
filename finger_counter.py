import cv2
import mediapipe as mp
import serial
import time
from collections import deque

ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

tips = [4, 8, 12, 16, 20]
cap = cv2.VideoCapture(0)

last_sent = -1
history = deque(maxlen=7)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    count = 0

    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:
            lm = hand_lms.landmark
            fingers = []
            fingers.append(1 if lm[tips[0]].x < lm[tips[0]-1].x else 0)
            for i in range(1, 5):
                fingers.append(1 if lm[tips[i]].y < lm[tips[i]-2].y else 0)
            count = fingers.count(1)
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
    else:
        count = 0

    history.append(count)

    # Only trust a value if it's the same for the last N frames (stable)
    if history.count(history[-1]) == len(history):
        stable_count = history[-1]
        if stable_count != last_sent:
            ser.write(f"{stable_count}\n".encode())
            last_sent = stable_count

    cv2.putText(frame, f"Fingers: {count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f"LED Count: {last_sent}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imshow("Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
