import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk

faceMeh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(0)
screenW, screenH = pyautogui.size()
factorX = 1.2
factorY = 1.3

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgbFace = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMeh.process(rgbFace)
    landmarkPoints = output.multi_face_landmarks
    frameH, frameW, _ = frame.shape
    cnt, prevX, prevY = 0, 0, 0

    if landmarkPoints:
        landmarks = landmarkPoints[0].landmark

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frameW)
            y = int(landmark.y * frameH)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screenX = screenW / frameW * x * factorX
                screenY = screenH / frameH * y * factorY
                # pyautogui.moveTo(screenX, screenY)
            left = [landmarks[145], landmarks[159]]




            for landmark in left:
                # x = int(landmark.x * frameW)
                # y = int(landmark.y * frameH)
                # cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.01:
                    pyautogui.click()
                    #pyautogui.sleep(1)

        dist1 = landmarks[411].x - landmarks[1].x
        dist2 = landmarks[411].x - landmarks[206].x
        if(dist1/dist2 > 0.80):
            pyautogui.move(-30,0)
        if(dist1/dist2 < 0.55):
            pyautogui.move(30,0)

        dist3 = landmarks[10].y - landmarks[1].y
        dist4 = landmarks[10].y - landmarks[152].y
        if(dist3/dist4 > 0.55):
            pyautogui.move(0,30)
        if(dist3/dist4 < 0.49):
            pyautogui.move(0,-30)



    cv2.imshow('Visioniyam', frame)
    cv2.waitKey(1)
