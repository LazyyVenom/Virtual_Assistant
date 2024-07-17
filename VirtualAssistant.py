# IMPORTING REQUIRED LIBRARIES
import cv2
import mediapipe as mp
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Importing Face Detector related Libraries
from FaceTracking import face_filter

# Importing Hand Detector And Additional Functions
from HandTracking import HandDetector

#Initializing IMP Vars
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def recognizeFingerJoin(hands: list[list[int]]) -> bool:
    # OPENING/CLOSING OPTIONS
    settingFlag = True
    for hand in hands:
        neededPoints = [4, 8, 12, 16, 20]
        for neededPoint in neededPoints:
            for neededPoint2 in neededPoints:
                if (
                    abs(hand[neededPoint][2] - hand[neededPoint2][2]) < 20
                    and abs(hand[neededPoint][1] - hand[neededPoint2][1]) < 45
                ):
                    continue
                else:
                    settingFlag = False

    return settingFlag


def transparent_circle(frame, center, radius, color, alpha=0.5):
    overlay = frame.copy()

    cv2.circle(overlay, center, radius, color, -1)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def transparent_rectangle(frame, x1, y1, x2, y2, color, alpha=0.5,boundary=cv2.FILLED):
    overlay = frame.copy()

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, boundary)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    return frame


def countFingers(hands: list[list[int]]) -> int:
    fingers = 0
    for hand in hands:
        fingerTips = [8, 12, 16, 20]
        for fingerTip in fingerTips:
            if hand[fingerTip][2] < hand[fingerTip - 2][2]:
                fingers += 1

        if hand[4][1] > hand[2][1]:
            fingers += 1

    return fingers


def volume_changer(length, img):
    volPer = np.interp(length, [0, 100], [0, 1])
    volBar = np.interp(length, [0, 100], [300, 60])

    volume.SetMasterVolumeLevelScalar(volPer, None)

    transparent_rectangle(img,575, 60, 600, 300, (100, 200, 0),boundary=3)
    transparent_rectangle(img,575, int(volBar), 600, 300, (255, 210, 0))
    cv2.putText(img, f'{int(volPer * 100)} %', (500, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 210, 0), 3)

    return img


def meter_manager(img, hands, type):
    if hands:
        pt1 = (hands[0][4][1], hands[0][4][2])
        pt2 = (hands[0][8][1], hands[0][8][2])
        img = cv2.line(img, pt1, pt2, (255, 210, 0), 5)
        img = cv2.circle(img, ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2), 8, (200, 130, 0), cv2.FILLED)
        img = cv2.circle(img, pt1, 8, (200, 130, 0), cv2.FILLED)
        img = cv2.circle(img, pt2, 8, (200, 130, 0), cv2.FILLED)

        length = int(np.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1]))

        if type == "V":
            img = volume_changer(length, img)
            return img
        elif type == "B":
            # Handle brightness adjustment here if needed
            pass

    return img


def volume_(img, hands):
    img = meter_manager(img, hands, type="V")
    return img


def brightness(img, hands):
    img = meter_manager(img, hands, type="B")
    return img


def gestures_control():
    print("Gestures Control")


def game_remote():
    print("Game Remote")


def main():
    """
    Main Working...
    """
    cap = cv2.VideoCapture(0)
    cap.set(4, 240)
    cap.set(5, 480)

    mp_face_detection = mp.solutions.face_detection

    handsDetector = HandDetector()
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.4
    )

    rotation_turn1 = 0
    rotation_turn2 = 8
    rotation_turn3 = 0

    pTime = 0
    cTime = 0

    settingFlag = False
    toggleTimer = 0
    sub_toggleTimer = 0
    selected = 0
    selected_already = False
    while True:
        _, img = cap.read()

        hands, img = handsDetector.giveAllPoints(img, connections=False)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        setting = False
        fingers = 0
        if hands:
            setting = recognizeFingerJoin(hands)
            if not selected_already:
                fingers = countFingers(hands)
            else:
                fingers = 0

        toggleTimer += 1 / fps

        if setting and toggleTimer >= 2:
            if selected != 0:
                selected = 0
            else:
                settingFlag = not settingFlag
            toggleTimer = 0
            selected_already = False
            if settingFlag:
                cv2.circle(img, (600, 20), 10, (0, 255, 0), cv2.FILLED)
            else:
                cv2.circle(img, (600, 20), 10, (0, 0, 255), cv2.FILLED)

        prev_img = img
        try:
            if settingFlag:
                if fingers == 1 or selected == 1:
                    sub_toggleTimer += 1 / fps
                    if sub_toggleTimer >= 2 and selected == 0:
                        sub_toggleTimer = 0
                        selected = 1
                        selected_already = True

                    if selected == 1:
                        gestures_control()

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        1,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                        not selected == 0
                    )

                elif fingers == 2 or selected == 2:
                    sub_toggleTimer += 1 / fps
                    if sub_toggleTimer >= 2 and selected == 0:
                        sub_toggleTimer = 0
                        selected = 2
                        selected_already = True

                    if selected == 2:
                        game_remote()

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        2,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                        not selected == 0
                    )

                elif fingers == 3 or selected == 3:
                    sub_toggleTimer += 1 / fps
                    if sub_toggleTimer >= 2 and selected == 0:
                        sub_toggleTimer = 0
                        selected = 3
                        selected_already = True

                    if selected == 3:
                        img = volume_(img, hands)

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        3,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                        not selected == 0
                    )
                elif fingers == 4 or selected == 4:
                    sub_toggleTimer += 1 / fps
                    if sub_toggleTimer >= 2 and selected == 0:
                        sub_toggleTimer = 0
                        selected = 4
                        selected_already = True

                    if selected == 4:
                        img = brightness(img, hands)

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        4,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                        not selected == 0
                    )

                elif fingers == 5:
                    sub_toggleTimer += 1 / fps
                    if sub_toggleTimer >= 2 and selected == 0:
                        sub_toggleTimer = 0
                        print("Exiting...")
                        exit()

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        5,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                        not selected == 0
                    )

                else:
                    sub_toggleTimer = 0

                    img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
                        face_detection,
                        0,
                        img,
                        True,
                        (rotation_turn1, rotation_turn2, rotation_turn3),
                    )

            else:
                img, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(face_detection, 0, img, False, (rotation_turn1, rotation_turn2, rotation_turn3))

        except TypeError:
            print("Problem in Reading Image")

        try:
            cv2.imshow("Virtual Assistant", img)
            cv2.moveWindow("Virtual Assistant", 200, 200)

        except:
            cv2.imshow("Virtual Assistant", prev_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()