# This is not Alex Lamarche's code.
# You can find the source below:
# https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import pyautogui
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 60)

width, height= pyautogui.size()
with mp_hands.Hands(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.2,
    min_tracking_confidence=0.8,) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    # image.flags.writeable = False
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    # image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
      #pyautogui.moveTo(-tip.x*width, tip.y*height)
      x,y = -tip.x*width, tip.y*height
      pyautogui.moveTo(-tip.x*width, tip.y*height)
      last_x,last_y = x,y
    # Flip the image horizontally for a selfie-view display.
    #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()