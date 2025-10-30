import cv2
import time
import serial

WEBCAM_INDEX = 0
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
CENTER_TOLERANCE = 50

# Connect to Arduino
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Arduino connected on {SERIAL_PORT}")
except:
    ser = None
    print("No Arduino – using simulation.")

def send(cmd):
    if ser and ser.is_open:
        ser.write(cmd.encode())
    else:
        print(f"[SIM] → {cmd}")

cap = cv2.VideoCapture(WEBCAM_INDEX)
if not cap.isOpened():
    print("Camera not opened")
    exit()

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if cascade.empty():
    print("Haar cascade not found!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))

    cmd = "S"  # default stop
    frame_center = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2

    if len(faces):
        x, y, w, h = max(faces, key=lambda r: r[2]*r[3])
        cx = x + w // 2

        # Only move if outside dead zone
        if cx < frame_center - CENTER_TOLERANCE:
            cmd = "L"
        elif cx > frame_center + CENTER_TOLERANCE:
            cmd = "R"
        else:
            cmd = "S"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame, (cx, y+h//2), 5, (0,255,0), -1)

    send(cmd)
    cv2.imshow("Face Tracker + Motor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser and ser.is_open:
    send("S")
    ser.close()
