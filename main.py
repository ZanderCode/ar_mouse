# This is not Alex Lamarche's code.
# You can find the source below:
# https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import mouse
import pyautogui
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

mp_hands = mp.solutions.hands

width, height = pyautogui.size()

preX = 0
preY = 0
curX = 0
curY = 0

isClicking = False
click_threshold = 20

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
                # Bottom knuckle of index finger
                index_knuck = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]

                # on screen distance ( not camera postion which is from 0 to 1 )
                click_dist_y = abs(index_tip.y*height - index_dip.y*height)
                click_dist_x = abs(index_tip.x*width - index_dip.x*width)

                tip_screen_y = index_tip.y*height
                dip_screen_y = index_dip.y*height

                if(tip_screen_y < dip_screen_y) and not isClicking:
                    mouse.release()
                    isClicking = True

                if(tip_screen_y > dip_screen_y) and isClicking:
                    mouse.press()
                    isClicking = False

                # The idea is that the previus position will influence
                # the next position according to some distance value
                # Dividing allows for a dampening effect.
                curX = preX + (index_knuck.x - preX) / 3
                curY = preY + (index_knuck.y - preY) / 3

                # TODO: send as bytes? prolly faster
                # TODO: couple custom json object send encoded so that we can send more data
                client.send(("x:" + str(width-(curX*width)) +
                            ", y:" + str(curY*height)).encode())

                mouse.move(width-(curX*width), curY*height)

                preX = curX
                preY = curY

        if cv2.waitKey(5) & 0xFF == 27:
            client.close()
            break
cap.release()
