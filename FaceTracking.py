import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # To improve performance, mark the image as not writeable to pass by reference
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                # Extract the bounding box
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                xmin = int(bboxC.xmin * iw)
                ymin = int(bboxC.ymin * ih)
                width = int(bboxC.width * iw)
                height = int(bboxC.height * ih)
                
                # Calculate center and radius for the circle
                center_x, center_y = int(xmin + width / 2), int(ymin + height / 2)
                radius = int(min(width, height) / 2)
                
                # Draw a circle around the face
                cv2.circle(image, (center_x, center_y), radius, (0, 255, 0), 2)
                
                # Draw key points
                for keypoint in detection.location_data.relative_keypoints:
                    keypoint_x = int(keypoint.x * iw)
                    keypoint_y = int(keypoint.y * ih)
                    cv2.circle(image, (keypoint_x, keypoint_y), 5, (0, 0, 255), -1)

                # Optionally, put a label with detection confidence
                cv2.putText(image, f'{int(detection.score[0] * 100)}%', (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Detection',image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        
cap.release()
cv2.destroyAllWindows()
