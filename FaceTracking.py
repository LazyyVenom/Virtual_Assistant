import cv2
import mediapipe as mp
from HandTracking import transparent_circle_boundary

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
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
                
                cv2.circle(image, (center_x, center_y - 20), radius, (0, 255, 0), 2)
                
                scale = radius / 90

                keypoints = list(detection.location_data.relative_keypoints)
                
                eyes = (keypoints[0],keypoints[1])

                color = (255,210,0)

                image = transparent_circle_boundary(image,((int(eyes[0].x * iw),int(eyes[0].y * ih))),int(25*scale),color,alpha=0.3,boundary=10)
                image = transparent_circle_boundary(image,((int(eyes[1].x * iw),int(eyes[1].y * ih))),int(25*scale),color,alpha=0.3,boundary=10)

        cv2.imshow('Trying Filter',image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        
cap.release()
cv2.destroyAllWindows()
