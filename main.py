# Import library yang diperlukan
import cv2 as cv
import mediapipe as mp
import pyttsx3 as tts
import time

lebarWajahAsli = float(input("Masukkan lebar wajah dalam cm (misal: 15): "))

# Inisialisasi MediaPipe Face Mesh
mp_faceMesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Fungsi Text-to-Speech
def speak(text):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Konfig Face Mesh
faceMesh = mp_faceMesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Buka Webcam
cap = cv.VideoCapture(0)

focalLength = None
jarak = None
lastSpeak = 0
while True:
    # Variabel untuk key input
    key = cv.waitKey(1) & 0xFF
    
    # Baca frame
    ret, frame = cap.read()
    
    if not ret:
        print("Gagal membuka webcam")
        break

    # Preprocessing (resize dan BGR ke RGB)
    frame = cv.resize(frame, (640, 480))
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = faceMesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_faceMesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )
            
            # Ambil Koordinat pipi Kiri dan Kanan, Lalu ubah ke satuan pixel
            pipiKiri = face_landmarks.landmark[234]
            xKiri = int(pipiKiri.x * frame.shape[1])
            yKiri = int(pipiKiri.y * frame.shape[0])

            pipiKanan = face_landmarks.landmark[454]
            xKanan = int(pipiKanan.x * frame.shape[1])
            yKanan = int(pipiKanan.y * frame.shape[0])

            # Hitung lebar wajah dengan rumus jarak Euclidean
            lebarWajahpx = ((xKanan-xKiri)**2 + (yKanan-yKiri)**2)**0.5
            if focalLength is not None:
                jarak = (lebarWajahAsli * focalLength) / lebarWajahpx
                print(f"Jarak: {jarak:.2f} cm")
            
            # Peringatan TTS
            if jarak is not None:
                if jarak < 59:
                    cv.putText(frame, "Too Close", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if time.time() - lastSpeak > 3:
                        speak("you are too close")
                        lastSpeak = time.time()

    # Ambil FocalLength
    if key == ord('c'):
        speak("range has been calibrated")
        focalLength = (lebarWajahpx * 60) / lebarWajahAsli
        
    cv.imshow('Webcam', frame)
    if key == ord('q'):
            break
    
cap.release()
cv.destroyAllWindows()