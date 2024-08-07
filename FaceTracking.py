import cv2
import mediapipe as mp
from additional_functions import (
    transparent_circle_boundary,
    transparent_sector,
    option_generator,
)

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def face_filter(
    face_detection,
    selected: int,
    image,
    setting_toggle,
    rotations,
    done_selecting=False,
):
    """
    To Apply Face Filter Image.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            xmin = int(bboxC.xmin * iw)
            ymin = int(bboxC.ymin * ih)
            width = int(bboxC.width * iw)
            height = int(bboxC.height * ih)

            rotation_turn1, rotation_turn2, rotation_turn3 = rotations

            center_x, center_y = int(xmin + width / 2), int(ymin + height / 2)
            radius = int(min(width, height) / 2)
            color = (255, 210, 0)

            scale = radius / 90

            keypoints = list(detection.location_data.relative_keypoints)

            eyes = (keypoints[0], keypoints[1])

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
                rotation_turn1 * 15,
                9,
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
                rotation_turn2 * 23,
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
                rotation_turn3 * 18,
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

            placement = [
                (int(eyes[0].x * iw) - 80, int(eyes[0].y * ih) - 90),
                (int(eyes[0].x * iw) - 30, int(eyes[0].y * ih) - 130),
                (int(eyes[0].x * iw) + 30, int(eyes[0].y * ih) - 140),
                (int(eyes[0].x * iw) + 90, int(eyes[0].y * ih) - 130),
                (int(eyes[0].x * iw) + 140, int(eyes[0].y * ih) - 90),
            ]

            symbol = ["G", "R", "V", "B", "X"]

            if setting_toggle and not done_selecting:
                # Option 1
                image = option_generator(
                    image,
                    placement[0],
                    text=symbol[0],
                    radius=int(30 * scale),
                    color=(100, 200, 0) if selected == 1 else (255, 210, 0),
                )

                # Option 2
                image = option_generator(
                    image,
                    placement[1],
                    text=symbol[1],
                    radius=int(30 * scale),
                    color=(100, 200, 0) if selected == 2 else (255, 210, 0),
                )

                # Option 3
                image = option_generator(
                    image,
                    placement[2],
                    text=symbol[2],
                    radius=int(30 * scale),
                    color=(100, 200, 0) if selected == 3 else (255, 210, 0),
                )

                # Option 4
                image = option_generator(
                    image,
                    placement[3],
                    text=symbol[3],
                    radius=int(30 * scale),
                    color=(100, 200, 0) if selected == 4 else (255, 210, 0),
                )

                # Option 5
                image = option_generator(
                    image,
                    placement[4],
                    text=symbol[4],
                    radius=int(30 * scale),
                    color=(100, 200, 0) if selected == 5 else (255, 210, 0),
                )

                # image = show_random_numbers_on_frame(image,100)
                if selected == 0:
                    cv2.putText(
                        image,
                        "G - Gestures Controlling, R - Game Remote, V - Volume, B - Brightness, X - Exit",
                        (7, 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.42,
                        (200, 130, 0),
                        1,
                        cv2.LINE_AA,
                    )

            if done_selecting:
                image = option_generator(
                    image,
                    (int(eyes[0].x * iw) + 30, int(eyes[0].y * ih) - 140),
                    text=symbol[selected - 1],
                    radius=int(30 * scale * 1.5),
                    color=(255, 210, 0),
                )

                image = transparent_circle_boundary(
                    image,
                    (int(eyes[0].x * iw) + 30, int(eyes[0].y * ih) - 140),
                    radius=int(30 * scale * 1.5),
                    color=(200, 130, 0),
                    alpha=0.7
                )

            return image, rotation_turn1, rotation_turn2, rotation_turn3
    return None  # Return None if no detections


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    face_detection = mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.4
    )

    rotation_turn1 = 0
    rotation_turn2 = 8
    rotation_turn3 = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image, rotation_turn1, rotation_turn2, rotation_turn3 = face_filter(
            face_detection,
            2,
            image,
            False,
            (rotation_turn1, rotation_turn2, rotation_turn3),
        )

        if image is not None and image.size != 0:
            cv2.imshow("Trying Filter", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
