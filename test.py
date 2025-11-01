import cv2
import time
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
time.sleep(1)
if not cap.isOpened():
    print("Camera not opened")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("No frame")
        break
    cv2.imshow("Camera Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# this file was used to debug camera issues