import cv2
import mediapipe as mp
import pyautogui
import mediapipe as mp

def initialize_camera():
    return cv2.VideoCapture(0)

def capture_frame(camera):
    _, frame = camera.read()
    return cv2.flip(frame, 1)

def process_frame(frame, face_mesh):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(rgb_frame)

def draw_landmark_points(frame, landmarks):
    frame_height, frame_width, _ = frame.shape
    for landmark in landmarks:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        cv2.circle(frame, (x, y), 3, (0, 255, 0))

def calculate_mouse_position(landmarks, screen_width, screen_height, factor_x, factor_y):
    x = int(landmarks[475].x * screen_width * factor_x)
    y = int(landmarks[475].y * screen_height * factor_y)
    return x, y

def left_eye_closed(left_eye_landmarks):
    return abs(left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.01

def control_mouse_click(landmarks):
    if left_eye_closed([landmarks[145], landmarks[159]]):
        pyautogui.click()

def move_mouse(dist1, dist2):
    if dist1 / dist2 > 0.80:
        pyautogui.move(-30, 0)
    if dist1 / dist2 < 0.55:
        pyautogui.move(30, 0)

def move_mouse_vertical(dist3, dist4):
    if dist3 / dist4 > 0.55:
        pyautogui.move(0, 30)
    if dist3 / dist4 < 0.49:
        pyautogui.move(0, -30)

def main():
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    camera = initialize_camera()
    screen_width, screen_height = pyautogui.size()
    factor_x = 1.2
    factor_y = 1.3

    while True:
        frame = capture_frame(camera)
        output = process_frame(frame, face_mesh)
        landmark_points = output.multi_face_landmarks

        if landmark_points:
            landmarks = landmark_points[0].landmark
            draw_landmark_points(frame, landmarks)
            mouse_x, mouse_y = calculate_mouse_position(landmarks, screen_width, screen_height, factor_x, factor_y)
            pyautogui.moveTo(mouse_x, mouse_y)
            control_mouse_click(landmarks)
            move_mouse(landmarks[411].x - landmarks[1].x, landmarks[411].x - landmarks[206].x)
            move_mouse_vertical(landmarks[10].y - landmarks[1].y, landmarks[10].y - landmarks[152].y)

        cv2.imshow('Visioniyam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
