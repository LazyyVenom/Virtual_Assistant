#IMPORTING REQUIRED LIBRARIES..
import cv2
import mediapipe as mp
import time
import math

#Importing HandDetector Class
from HandRecognition import HandDetector


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    cap.set(4,240)
    cap.set(5,480)

    handsDetector = HandDetector()

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()

        hands,img = handsDetector.giveAllPoints(img,connections=False)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        print(hands)

        cv2.putText(img,f"FPS: {int(fps)}", (10,40), cv2.FONT_HERSHEY_PLAIN,2,(0,0,255))
        cv2.imshow("Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break