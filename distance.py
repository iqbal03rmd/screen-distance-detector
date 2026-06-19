def hitungFocalLength(lebarWajahpx, lebarWajahAsli, jarakKalibrasi=60):
    return (lebarWajahpx * jarakKalibrasi) / lebarWajahAsli

def hitungJarak(lebarWajahAsli, focalLength, lebarWajahpx):
    return (lebarWajahAsli * focalLength) / lebarWajahpx

def hitungLebarWajahpx(face_landmarks, frame_shape):
    pipiKiri = face_landmarks.landmark[234]
    xKiri = int(pipiKiri.x * frame_shape[1])
    yKiri = int(pipiKiri.y * frame_shape[0])

    pipiKanan = face_landmarks.landmark[454]
    xKanan = int(pipiKanan.x * frame_shape[1])
    yKanan = int(pipiKanan.y * frame_shape[0])

    return ((xKanan - xKiri)**2 + (yKanan - yKiri)**2)**0.5