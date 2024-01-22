#IMPORTING REQUIRED LIBRARIES FOR HAND RECOGNITION...
import cv2
import mediapipe as mp
import time

#LETS DO IT OOPS STYLE
class Hand_Recognizer():
    def __init__(self) -> None:
        pass

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                print(f"Point {id}: ({cx}, {cy})")
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

            mp.solutions.drawing_utils.draw_landmarks(
                img, hand_landmarks)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()