import cv2
import face_recognition
import time
import os
import numpy as np

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
know_face_encodings = []
know_face_names = []

def run_face_detection(args):
    # TODO: meant to be enables/disabled by menu icon
    #load_facial_recognition()

    lock_delay = args.sec

    # TODO: have in README
    # 0 or 1 based on Continous Camera
    camera_index = 1

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(camera_index)

    if not video.isOpened():
        print(f"Failed to access camera (index {camera_index})")
        return

    last_seen_time = time.time()
    print(f"FaceLock started. Locking after {lock_delay}s of no face.")

    while True:
        ret, frame = video.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # TODO: temp / fjern
        #use_facial_recognition(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # For debugging, cant run with menu_icon or with osascript
        display_camera(cv2, faces, frame, face_locations, face_names)

        # TODO: denne må sammenligne med om jeg er sett, ikke len(faces)
        if len(faces) > 0:
            last_seen_time = time.time()
        

        if time.time() - last_seen_time > lock_delay:
            print("No face detected — locking screen.")
            os.system("pmset displaysleepnow")
            # os.system("""osascript -e 'tell application "System Events" to keystroke "q" using {control down, command down}'""")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting FaceLock.")
            break

    video.release()
    cv2.destroyAllWindows()

def display_camera(cv2, faces, frame, face_locations, face_names):
    # Without Facial Recognition
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("FaceLock - Press Q to quit", frame)
    
    '''
    # With Facial Recognition
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
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

    # Display the resulting image
    cv2.imshow('FaceLock - Press Q to quit', frame)
    '''

def load_facial_recognition():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_image_path = os.path.join(script_dir, "marco_josefsen.jpg")

    user_image = face_recognition.load_image_file(user_image_path)
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    known_face_encodings = [
        user_face_encoding,
    ]
    known_face_names = [
        "Marco Josefsen",
    ]

def use_facial_recognition(frame):
    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Get face bounding boxes
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Get encodings from bounding boxes (not landmarks!)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                # TODO: la til denne for å oppdatere tid her, men den detecter ikke meg
                #last_seen_time = time.time()

            face_names.append(name)

        process_this_frame = not process_this_frame