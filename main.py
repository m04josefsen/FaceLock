import threading
from face_lock import face_lock, menu_icon
import argparse

if __name__ == "__main__":
    # face_lock.run_face_detection()
    
    # Run face detection in background thread
    cam_thread = threading.Thread(target=face_lock.run_face_detection, daemon=True)
    cam_thread.start()

    menu_icon.MenuIcon().run()
    