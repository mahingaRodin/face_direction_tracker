#!/usr/bin/env python3
import cv2
import time
import math 

#u're free to tune these parameters
WEBCAM_INDEX = 0            # change if your webcam is on another index
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_FACE_SIZE = (80, 80)    # minimum face size to consider
MOVEMENT_THRESHOLD_PX = 6   # small movements below this are treated as stationary
TEXT_SCALE = 0.7
TEXT_THICKNESS = 2

def largest_face(faces):
    if len(faces) == 0:
        return None
    return max(faces, key=lambda r: r[2] * r[3])

def direction_from_delta(dx,dy, threshold):
    adx = abs(dx)
    ady = abs(dy)
    
    if adx < threshold and ady < threshold:
        return "Stationary"
    if adx > ady:
        return "Right" if dx > 0 else "Left"
    else:
        return "Down" if dy > 0 else "Up"
    

def main():
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        raise RuntimeError("Failed to load Haar cascade from: " + cascade_path)

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam (index {}).".format(WEBCAM_INDEX))

    prev_center = None
    prev_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: frame not read from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_FACE_SIZE
        )

        chosen = largest_face(faces)
        now = time.time()
        direction = "No face"
        speed_px_s = 0.0

        if chosen is not None:
            x, y, w, h = chosen
            cx = x + w // 2
            cy = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

            if prev_center is not None and prev_time is not None:
                dx = cx - prev_center[0]
                dy = cy - prev_center[1]
                dt = now - prev_time
                if dt <= 0:
                    dt = 1e-6
             
                speed_px_s = math.hypot(dx, dy) / dt

                direction = direction_from_delta(dx, dy, MOVEMENT_THRESHOLD_PX)
            else:
                direction = "Tracking..."
                speed_px_s = 0.0

            prev_center = (cx, cy)
            prev_time = now

           
            label = f"Dir: {direction} | Speed: {speed_px_s:.0f} px/s"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        TEXT_SCALE, (0, 255, 0), TEXT_THICKNESS, cv2.LINE_AA)

            cv2.putText(frame, f"({cx},{cy})", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0,255,0), 1, cv2.LINE_AA)
        else:
            
            prev_center = None
            prev_time = None
            cv2.putText(frame, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2, cv2.LINE_AA)

        # Display frame
        cv2.imshow("Face Direction Tracker", frame)

        # quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
