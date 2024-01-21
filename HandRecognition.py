import cv2
import mediapipe as mp
import time

# Check if CUDA is available
cv2.setUseOptimized(True)
cv2.setNumThreads(8)
cv2.ocl.setUseOpenCL(True)
cv2.cuda.setDevice(0)  # Set the GPU device index

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

while True:
    success, img = cap.read()

    # Upload the image to the GPU
    img_gpu = cv2.cuda_GpuMat()
    img_gpu.upload(img)

    # Perform color conversion on the GPU
    imgRGB_gpu = cv2.cuda.cvtColor(img_gpu, cv2.COLOR_BGR2RGB)

    # Download the result back to the CPU
    imgRGB = imgRGB_gpu.download()

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                img, hand_landmarks, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
