import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 7000

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(1)
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
      image_height, image_width, _ = image.shape
      annotated_image = image.copy()

      # k = 0
      for hand_landmarks in results.multi_hand_landmarks:
        # print('hand_landmarks:', hand_landmarks)
        # print(
        #     f'Index finger tip coordinates: (',
        #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
        # )

        #Send message to TouchDesigner
        msg = str(hand_landmarks)
        sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
  
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.

    # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()