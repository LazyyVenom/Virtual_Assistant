#IMPORTING REQUIRED LIBRARIES FOR HAND RECOGNITION...
import cv2
import mediapipe as mp
import time
import math

from additional_functions import transparent_circle


#LETS DO IT OOPS STYLE
class HandDetector():
    def __init__(self,mode=False,numOfHands=2,complexity=1,minConfidence=0.7) -> None:
        self.mode = mode
        self.numOfHands = numOfHands
        self.complexity = complexity
        self.minConfidence = minConfidence

        self.mpHands = mp.solutions.hands
        self.mpDraws = mp.solutions.drawing_utils

        self.hands = self.mpHands.Hands(
            self.mode, self.numOfHands, self.complexity, self.minConfidence
        )


    def giveAllPoints(self, img, color: tuple = (255,210,0), draw: bool = True,connections: bool = True):
        """
        Will Give All the 21 Points of the hand.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(imgRGB)

        hands = []
        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                bcUpper = [0,0]
                bcLower = [0,0]
                points = []

                for id, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    # print(f"Point {id}: ({cx}, {cy})")
                    points.append([id,cx,cy])

                    if draw:
                        if id == 0:
                            bcLower = [cx,cy]
                        
                        elif id == 5:
                            bcUpper = [cx,cy]

                        if id in [4,8,12,16,20]:
                            cv2.circle(img, (cx, cy), 10, color)
                            img = transparent_circle(img,(cx,cy),10,color)

                if draw:
                    big_circle_pts, big_circle_radius = (), 0
                    if points[4][1] > points[20][1]:
                        big_circle_pts = (((bcLower[0]+bcUpper[0])//2 - 6),
                                    ((bcLower[1]+bcUpper[1])//2) - 5)

                        big_circle_radius = int(math.sqrt((bcUpper[1] - bcLower[1])**2 +
                                                    (bcUpper[0] - bcLower[0])**2) // 2) - 4
                        
                    else:
                        big_circle_pts = (((bcLower[0]+bcUpper[0])//2 + 6),
                                    ((bcLower[1]+bcUpper[1])//2) - 5)

                        big_circle_radius = int(math.sqrt((bcUpper[1] - bcLower[1])**2 +
                                                    (bcUpper[0] - bcLower[0])**2) // 2) - 4

                    cv2.circle(img, big_circle_pts, int(big_circle_radius*0.9), color,2)
                    img = transparent_circle(img,big_circle_pts,int(big_circle_radius*0.9),color)

                if connections:
                    self.mpDraws.draw_landmarks(
                            img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

                hands.append(points)
        
        return hands,img


def recognizeFingerJoin(hands : list[list[int]]):
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
        
    if settingFlag:
        return True

    return False



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

        if hands:
            setting = recognizeFingerJoin(hands)

        toggleTimer += 1 / fps

        if setting and toggleTimer >= 3:
            settingFlag = not settingFlag
            toggleTimer = 0
            if settingFlag:
                cv2.circle(img,(600,20),10,(0,255,0),cv2.FILLED)
            else:
                cv2.circle(img,(600,20),10,(0,0,255),cv2.FILLED)

        if settingFlag:
            cv2.putText(img,"Settings", (100,100),cv2.FONT_HERSHEY_COMPLEX,2,color=(0,255,0))

        cv2.putText(img,f"FPS:{int(fps)}", (10,40), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255))
        cv2.imshow("Hand Tracking", img)
        cv2.moveWindow("Hand Tracking", 100, 200)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()