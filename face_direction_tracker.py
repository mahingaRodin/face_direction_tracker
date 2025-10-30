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