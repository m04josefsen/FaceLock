import cv2
import time
import os

def run_face_detection(args):
    lock_delay = args.sec

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

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # For debugging, cant run with menu_icon or with osascript
        '''
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("FaceLock - Press Q to quit", frame)
        '''

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