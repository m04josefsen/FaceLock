import cv2
import face_recognition
import time
import os
import numpy as np
from face_lock import settings

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
known_face_encodings = []
known_face_names = []
last_seen_time = time.time()

def run_face_detection():
    global last_seen_time
    has_loaded_facial_recognition = False

    # 0 or 1 based on Continous Camera
    camera_index = 1
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(camera_index)

    if not video.isOpened():
        print(f"Failed to access camera (index {camera_index})")
        return

    last_seen_time = time.time()

    while True:
        if not has_loaded_facial_recognition and settings.use_facial_recognition:
            load_facial_recognition()
            has_loaded_facial_recognition = True

        lock_delay = settings.selected_delay

        ret, frame = video.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        if settings.use_facial_recognition:
            process_facial_recognition(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # For debugging, cant run with menu_icon or with osascript
        # display_camera(cv2, faces, frame, face_locations, face_names)

        # If we are not using facial recognition, only detect amount of faces
        if not settings.use_facial_recognition:
            if len(faces) > 0:
                last_seen_time = time.time()
        
        if time.time() - last_seen_time > lock_delay:
            print("No face detected — locking screen.")
            # os.system("pmset displaysleepnow")
            os.system("""osascript -e 'tell application "System Events" to keystroke "q" using {control down, command down}'""")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting FaceLock.")
            break

    video.release()
    cv2.destroyAllWindows()

def display_camera(cv2, faces, frame, face_locations, face_names):
    '''
    # Without Facial Recognition
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("FaceLock - Press Q to quit", frame)
    '''
    
    # With Facial Recognition
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations from 1/4
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('FaceLock - Press Q to quit', frame)
    

def load_facial_recognition():
    global known_face_encodings, known_face_names

    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_image_path = os.path.join(script_dir, "user.jpg")

    user_image = face_recognition.load_image_file(user_image_path)
    encodings = face_recognition.face_encodings(user_image)

    if not encodings:
        raise ValueError("No face found in the training image")
    
    user_face_encoding = encodings[0]

    known_face_encodings.append(user_face_encoding)
    known_face_names.append("user")

def process_facial_recognition(frame):
    global face_locations, face_encodings, face_names
    global process_this_frame
    global known_face_encodings, known_face_names
    global last_seen_time

    # Based on: https://github.com/ageitgey/face_recognition?tab=readme-ov-file
    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Get face bounding boxes
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Only proceed if faces are found
        face_names = []
        if face_locations:
            try:
                rgb_small_frame = rgb_small_frame.astype(np.uint8)
                
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    if known_face_encodings: 
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            # Update last seen time when a known face is detected
                            last_seen_time = time.time()

                    face_names.append(name)
            except Exception as e:
                print(f"Error in facial recognition processing: {e}")
                # If facial recognition fails, fall back to simple face detection
                if face_locations:
                    last_seen_time = time.time()
                face_encodings = []
                face_names = ["Face Detected" for _ in face_locations]
        else:
            face_encodings = []

    process_this_frame = not process_this_frame