#IMPORTING REQUIRED LIBRARIES
import cv2
import mediapipe as mp
import time
import math


#Importing Hand Detector And Additional Functions
from HandRecognition import HandDetector

def recognizeFingerJoin(hands : list[list[int]]) -> bool: 
    #OPENING/CLOSING OPTIONS 
    settingFlag = True
    for hand in hands:
        neededPoints = [4,8,12,16,20]
        for neededPoint in neededPoints:
            for neededPoint2 in neededPoints:
                if abs(hand[neededPoint][2] - hand[neededPoint2][2]) < 20:
                    continue
                else:
                    settingFlag = False
        
    return settingFlag


def transparent_circle(frame,center,radius,color, alpha = 0.5):
    overlay = frame.copy()
    
    cv2.circle(overlay, center, radius, color, -1)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def transparent_rectangle(frame,x1,y1,x2,y2,color,alpha = 0.5):
    overlay = frame.copy()
    
    cv2.rectangle(frame,(x1,y1),(x2,y2),color,cv2.FILLED)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def countFingers(hands : list[list[int]]) -> int:
    fingers = 0
    for hand in hands:
        fingerTips = [8,12,16,20]
        for fingerTip in fingerTips:
            if hand[fingerTip][2] < hand[fingerTip-2][2]:
                fingers += 1

        if hand[4][1] > hand[2][1]:
            fingers += 1

    return fingers


def main():
    """
    Sample Of How You Should Use These Functions.
    """
    cap = cv2.VideoCapture(0)

    cap.set(4,240)
    cap.set(5,480)

    handsDetector = HandDetector()

    pTime = 0
    cTime = 0

    settingFlag = False
    toggleTimer = 0
    while True:
        _, img = cap.read()

        hands,img = handsDetector.giveAllPoints(img,connections=False)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        setting = False

        fingers = 0
        if hands:
            setting = recognizeFingerJoin(hands)
            fingers = countFingers(hands)

        toggleTimer += 1 / fps

        if setting and toggleTimer >= 3:
            settingFlag = not settingFlag
            toggleTimer = 0
            if settingFlag:
                cv2.circle(img,(600,20),10,(0,255,0),cv2.FILLED)
            else:
                cv2.circle(img,(600,20),10,(0,0,255),cv2.FILLED)

        if settingFlag:
            img = transparent_rectangle(img,5,70,240,230,(25,60,100))
            if fingers == 1:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(255,0,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
            
            elif fingers == 2:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(255,0,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
            
            elif fingers == 3:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(255,0,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
            
            elif fingers == 4:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(255,0,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
            
            elif fingers == 5:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(255,0,0))
            
            else:
                cv2.putText(img,"Volume", (10,100),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"Brightness", (10,130),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"IronMan Mode", (10,160),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"PC Settings", (10,190),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))
                cv2.putText(img,"File Manager", (10,220),cv2.FONT_HERSHEY_PLAIN,2,color=(0,255,0))


        cv2.putText(img,f"FPS:{int(fps)}", (30,30), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255))
        cv2.imshow("Hand Tracking", img)
        cv2.moveWindow("Hand Tracking", 100, 200)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()