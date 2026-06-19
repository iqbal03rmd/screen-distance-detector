import cv2 as cv
import mediapipe as mp

mp_faceMesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def initFaceMesh():
    return mp_faceMesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

def initCamera():
    return cv.VideoCapture(0)

def drawLandmarks(frame, face_landmarks):
    mp_drawing.draw_landmarks(
        image=frame,
        landmark_list=face_landmarks,
        connections=mp_faceMesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
    )