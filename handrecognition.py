import cv2
import mediapipe as mp
import math
import os
from math import atan2, degrees

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.6) as hands:
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
      if len(results.multi_hand_landmarks) == 2:
        thumb_point_0 = results.multi_hand_landmarks[0].landmark[4]
        thumb_point_1 = results.multi_hand_landmarks[1].landmark[4]

        thumb_point_0_x, thumb_point_0_y = thumb_point_0.x, thumb_point_0.y
        thumb_point_1_x, thumb_point_1_y = thumb_point_1.x, thumb_point_1.y

        handle_angle = atan2(thumb_point_0_x- thumb_point_1_x, thumb_point_0_y-thumb_point_1_y)
        handle_angle = degrees(handle_angle) # 80 and 100 , mid is 90
        
        # if abs(handle_angle)<70:
        #   keyboard.press_and_release('left')
        #   print('left')
        # elif abs(handle_angle)>120:
        #   keyboard.press_and_release('right')
        #   print('right')
 


      for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
        

        fingers = []
        fingerValues = [
        #thumb
        hand_landmarks.landmark[4],
        hand_landmarks.landmark[2],
        #index
        hand_landmarks.landmark[8],
        hand_landmarks.landmark[5],
        #middle
        hand_landmarks.landmark[12],
        hand_landmarks.landmark[9],
        #ring
        hand_landmarks.landmark[16],
        hand_landmarks.landmark[13],
        #pinky
        hand_landmarks.landmark[20],
        hand_landmarks.landmark[17]]
        x = 0
        for i in range(5):
            finger_tip_x, finger_tip_y = (1-fingerValues[x].x)*640, fingerValues[x].y * 480
            x += 1
            finger_mcp_x, finger_mcp_y = (1-fingerValues[x].x)*640, fingerValues[x].y * 480
            x += 1
            localDistance = math.dist((finger_tip_x,finger_tip_y),(finger_mcp_x,finger_mcp_y))
            fingers.append([finger_tip_x, finger_tip_y, finger_mcp_x, finger_mcp_y, localDistance])

        #Make exception for thumb
        c1 = round(math.sqrt((fingers[1][2]-fingers[0][0])**2 + (fingers[1][3]-fingers[0][1])**2))
        c2 = round(math.sqrt((fingers[1][2]-fingers[0][2])**2 + (fingers[1][3]-fingers[0][3])**2))
        c3 = round(math.sqrt((fingers[0][2]-fingers[0][0])**2 + (fingers[0][1]-fingers[0][3])**2))
        num = pow(c1,2)-pow(c2,2)-pow(c3,2)
        den = (2)*(c2)*(c3)
        
        try:
            thumb_to_indx_angle = degrees(math.acos(num/den))
        except:
           thumb_to_indx_angle = 90

        thumb_to_indx_angle = 10000/thumb_to_indx_angle
        fingers[0][4] = thumb_to_indx_angle
        threshholds = [85, 50, 60, 70, 50]

        fingers_open = []
        for i, x in enumerate(fingers):
            if x[4] < threshholds[i]:
                fingers_open.append(False)
            else:
                fingers_open.append(True)

        gestures = ["zero", "one", "two", "three", "four", "five", "ready", "l"]
        finger_combs = [
            [False, False, False, False, False], 
            [False, True, False, False, False],
            [False, True, True, False, False],
            [False, True, True, True, False],
            [False, True, True, True, True],
            [True, True, True, True, True],
            [True, False, False, False, False],
            [True, True, False, False, False]
        ]

        if fingers_open in finger_combs:
            index = finger_combs.index(fingers_open)
            gesture = gestures[index]
        else:
           gesture = "none"
        
        print(gesture)

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    absolute_path = os.path.join(os.getcwd(), 'DSC_1902.JPG')
    
    cv2.imwrite(absolute_path,image)

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()


def recognize_sign(results):
  
  pass