#IMPORTING REQUIRED LIBRARIES FOR HAND RECOGNITION...
import cv2
import mediapipe as mp
import time
import math

#LETS DO IT OOPS STYLE
class Hand_Recognizer():
    def __init__(self) -> None:
        pass

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraws = mp.solutions.drawing_utils
hands = mpHands.Hands()

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            bcUpper = [0,0]
            bcLower = [0,0]
            for id, landmark in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                print(f"Point {id}: ({cx}, {cy})")

                if id == 0:
                    bcLower = [cx,cy]
                
                if id == 5:
                    bcUpper = [cx,cy]

                if id in [4,8,12,16,20]:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            
            big_circle_pts = (((bcLower[0]+bcUpper[0])//2),
                              ((bcLower[1]+bcUpper[1])//2) )

            big_circle_radius = int(math.sqrt((bcUpper[1] - bcLower[1])**2 +
                                          (bcUpper[0] - bcLower[0])**2) // 2)

            cv2.circle(img, big_circle_pts, big_circle_radius, (255,0,255), cv2.FILLED)

            print(f"LOWER INDEX-0:{bcLower}")
            print(f"UPPER INDEX-5:{bcUpper}")
            print(f"BIG CIRCLE POINTS:{big_circle_pts}")
            print(f"BIG CIRCLE RADIUS:{big_circle_radius}")

            mpDraws.draw_landmarks(
                img, hand_landmarks, mpHands.HAND_CONNECTIONS)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255))
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()