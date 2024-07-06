import cv2
import mediapipe as mp
from additional_functions import transparent_circle_boundary, transparent_sector

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.4
) as face_detection:
    
    rotation_turn1 = 0
    rotation_turn2 = 8
    rotation_turn3 = 0

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                xmin = int(bboxC.xmin * iw)
                ymin = int(bboxC.ymin * ih)
                width = int(bboxC.width * iw)
                height = int(bboxC.height * ih)

                center_x, center_y = int(xmin + width / 2), int(ymin + height / 2)
                radius = int(min(width, height) / 2)

                # cv2.circle(image, (center_x, center_y - 20), radius, (0, 255, 0), 2)

                scale = radius / 90

                keypoints = list(detection.location_data.relative_keypoints)

                eyes = (keypoints[0], keypoints[1])

                color = (255, 210, 0)

                image = transparent_circle_boundary(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(25 * scale),
                    color,
                    alpha=0.1,
                    boundary=5,
                )

                image = transparent_sector(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(25 * scale),
                    color,
                    rotation_turn1*15,
                    12,
                    alpha=0.7,
                    thickness=5,
                )

                image = transparent_circle_boundary(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(36 * scale),
                    color,
                    alpha=0.1,
                    boundary=5,
                )

                image = transparent_sector(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(36 * scale),
                    color,
                    rotation_turn2*23,
                    10,
                    alpha=0.7,
                    thickness=5,
                )

                image = transparent_circle_boundary(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(47 * scale),
                    color,
                    alpha=0.06,
                    boundary=-1,
                )

                image = transparent_circle_boundary(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(47 * scale),
                    color,
                    alpha=0.1,
                    boundary=5,
                )

                image = transparent_sector(
                    image,
                    ((int(eyes[0].x * iw), int(eyes[0].y * ih))),
                    int(47 * scale),
                    color,
                    rotation_turn3*18,
                    8,
                    alpha=0.7,
                    thickness=5,
                )

                rotation_turn1 += 1
                rotation_turn1 = rotation_turn1 % 24
                rotation_turn2 -= 1
                rotation_turn2 = rotation_turn2 if rotation_turn2 > 0 else 16
                rotation_turn3 += 1
                rotation_turn3 = rotation_turn3 % 20

        cv2.imshow("Trying Filter", image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
