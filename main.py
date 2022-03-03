# This is not Alex Lamarche's code.
# You can find the source below:
# https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import mouse
import pyautogui
from scipy.signal import savgol_filter

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

width, height= pyautogui.size()


max_amt = 19
x = [1] * (max_amt+1)
y = [1] * (max_amt+1)
# These are to calculate the smoothing of the noise of the mouse positions s
def filter_pos_noise_smooth(noise_x,noise_y):
  
  x.append(noise_x)
  y.append(noise_y)

  y_filt = savgol_filter(y[-(max_amt+1):-1],max_amt,4)
  x_filt = savgol_filter(x[-(max_amt+1):-1],max_amt,4)

  return x_filt[-1],y_filt[-1]

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

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        #pyautogui.moveTo(-tip.x*width, tip.y*height)
        
        noise_x,noise_y = tip.x, tip.y
        filt_x,filt_y = filter_pos_noise_smooth(noise_x,noise_y)
        mouse.move(-filt_x*width, filt_y*height)

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()