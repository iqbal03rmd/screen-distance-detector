import cv2 as cv
import time
import threading

from camera import initFaceMesh, initCamera, drawLandmarks
from distance import hitungFocalLength, hitungJarak, hitungLebarWajahpx
from tts import speak

lebarWajahAsli = float(input("Masukkan lebar wajah dalam cm (misal: 15): "))

faceMesh = initFaceMesh()
cap = initCamera()

focalLength = None
jarak = None
lastSpeak = 0

while True:
    key = cv.waitKey(1) & 0xFF
    ret, frame = cap.read()

    if not ret:
        print("Gagal membuka webcam")
        break

    frame = cv.resize(frame, (640, 480))
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = faceMesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            drawLandmarks(frame, face_landmarks)

            lebarWajahpx = hitungLebarWajahpx(face_landmarks, frame.shape)

            if focalLength is not None:
                jarak = hitungJarak(lebarWajahAsli, focalLength, lebarWajahpx)
                cv.putText(frame, f"Jarak: {jarak:.1f} cm", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if jarak is not None and jarak < 59:
                cv.putText(frame, "Too Close", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if time.time() - lastSpeak > 3:
                    threading.Thread(target=speak, args=("you are too close",)).start()
                    lastSpeak = time.time()

    if key == ord('c') and lebarWajahpx is not None:
        threading.Thread(target=speak, args=("range has been calibrated",)).start()
        focalLength = hitungFocalLength(lebarWajahpx, lebarWajahAsli)

    cv.imshow('Webcam', frame)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()