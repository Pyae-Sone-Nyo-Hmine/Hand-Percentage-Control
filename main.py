import mediapipe as mp
import cv2
import math
import numpy as np

# initializing hand detection from library
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# use webcam as camera
cap = cv2.VideoCapture(0)

while True:

    # read image
    success, image = cap.read()
    height, width, _ = image.shape
    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect points on hand
    results = hands.process(image_RGB)

    if results.multi_hand_landmarks:

        # specific points to be using for calculation
        thumb = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].x * width), \
                int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)

        index_finger = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width), \
                       int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

        pinky_mcp = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.PINKY_MCP].x * width), \
                    int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.PINKY_MCP].y * height)

        wrist = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST].x * width), \
                int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST].y * height)

        distance_1 = math.sqrt(((thumb[0] - index_finger[0]) ** 2) + ((thumb[1] - index_finger[1]) ** 2))
        distance_2 = math.sqrt(((pinky_mcp[0] - wrist[0]) ** 2) + ((pinky_mcp[1] - wrist[1]) ** 2))

        distance = int((distance_1 / distance_2) * 60) - 15
        distance = np.clip(distance, 0, 100)

        # draw points on showing opencv gui
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # draw extra dots and lines for extra clarification
        cv2.circle(image, thumb, 0, (255, 0, 0), 20)
        cv2.circle(image, index_finger, 0, (255, 0, 0), 20)
        cv2.line(image, thumb, index_finger, (255, 0, 0), 3)

    else:
        distance = 0

    # to flip the image
    image = cv2.flip(image, 1)

    cv2.putText(image, str(distance), (60, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 165, 255), 3, cv2.LINE_AA)

    cv2.imshow("Hand", image)

    cv2.waitKey(1)
