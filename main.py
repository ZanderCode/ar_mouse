# This is not Alex Lamarche's code.
# You can find the source below:
# https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import mouse
import pyautogui

mp_hands = mp.solutions.hands

width, height= pyautogui.size()

preX = 0
preY = 0
curX = 0
curY = 0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        index_knuck = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP] # Bottom knuckle of index finger
        
        # The idea is that the previus position will influence
        # the next position according to some distance value
        # Dividing allows for a dampening effect.
        curX = preX + (index_knuck.x - preX) / 3
        curY = preY + (index_knuck.y - preY) / 3

        mouse.move(-curX*width, curY*height)

        preX = curX
        preY = curY 

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()