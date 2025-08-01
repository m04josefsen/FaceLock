import cv2
import time
import os

'''
Current TODO list:
    - Facial recognition
    - Seconds as input, but keep 5 as standard
    - pystray for menu bar
'''

# Load the face detection model (Haar cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Index might be 0 or 1, depending on "Continuity camera"
camera_index = 0
video = cv2.VideoCapture(camera_index)

if not video.isOpened():
    print(f"Failed to access camera (index {camera_index})")
    exit()

lock_delay = 5 # sec
last_seen_time = time.time()

print(f"AutoLock started. Locking after {lock_delay}s of no face.")

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to read frame from webcam.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Show webcam feed
    # TODO: for debugging
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("AutoLock - Press Q to quit", frame)

    # Update last seen time
    if len(faces) > 0:
        last_seen_time = time.time()

    # If no faces seen for x seconds
    if time.time() - last_seen_time > lock_delay:
        print("No face detected")
        os.system("pmset displaysleepnow")
        break

    # Exit manually with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting AutoLock.")
        break

video.release()
cv2.destroyAllWindows()