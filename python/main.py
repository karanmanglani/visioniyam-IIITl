import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk

class MouseController:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.camera = cv2.VideoCapture(0)
        self.screen_width, self.screen_height = pyautogui.size()
        self.factor_x = 1.2
        self.factor_y = 1.3
        self.running = False

    def start(self):
        self.running = True
        self.capture()

    def stop(self):
        self.running = False

    def capture(self):
        if self.running:
            ret, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.face_mesh.process(rgb_frame)
            if output.multi_face_landmarks:
                landmarks = output.multi_face_landmarks[0].landmark
                self.change_mouse_position(landmarks)
                # Displaying Left Eye Points for denoting Click
                x = int(landmarks[475].x * frame_width)
                y = int(landmarks[475].y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

                x = int(landmarks[474].x * frame_width)
                y = int(landmarks[474].y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

                self.left_click([landmarks[475], landmarks[474]])

                # Displaying Right Eye points for denoting click
                x = int(landmarks[145].x * frame_width)
                y = int(landmarks[145].y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

                x = int(landmarks[159].x * frame_width)
                y = int(landmarks[159].y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

                self.right_click([landmarks[145], landmarks[159]])
            self.display_frame(frame)
            self.root.after(10, self.capture)

    def change_mouse_position(self, landmarks):
        dist1 = landmarks[411].x - landmarks[1].x
        dist2 = landmarks[411].x - landmarks[206].x
        if (dist1 / dist2 > 0.80):
            pyautogui.move(-30, 0)
        if (dist1 / dist2 < 0.55):
            pyautogui.move(30, 0)

        dist3 = landmarks[10].y - landmarks[1].y
        dist4 = landmarks[10].y - landmarks[152].y
        if (dist3 / dist4 > 0.55):
            pyautogui.move(0, 30)
        if (dist3 / dist4 < 0.49):
            pyautogui.move(0, -30)

    def left_click(self, left):
        for landmark in left:
            #print(left[1].y - left[0].y)
            if (left[1].y - left[0].y) < 0.013:
                pyautogui.click()

    def right_click(self, right):
        for landmark in right:
            #print(left[1].y - left[0].y)
            if (right[1].y - right[0].y) < 0.013:
                pyautogui.click()

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        self.img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video_panel.config(image=self.img)

    def run(self):
        self.root = tk.Tk()
        self.root.title("Face Controlled Mouse")

        self.start_btn = tk.Button(self.root, text="Start", command=self.start)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_btn.pack(pady=5)

        self.video_panel = tk.Label(self.root)
        self.video_panel.pack()

        self.root.mainloop()

if __name__ == "__main__":
    mouse_controller = MouseController()
    mouse_controller.run()
