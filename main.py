import threading
from face_lock import face_lock, menu_icon
import argparse

'''
Current TODO list:
    - Facial recognition
    X Seconds as input, but keep 5 as standard
    - Secomnd input in menubar?
    X Actually locking screen when no face is detected
    - Program doesnt stop after locking screen
'''

if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser(description="TODO:")
    parser.add_argument("-s", "--sec", type=int, default=5, help="Lock Delay seconds")
    args = parser.parse_args()
    '''

    #face_lock.run_face_detection()

    
    # Run face detection in background thread
    cam_thread = threading.Thread(target=face_lock.run_face_detection, daemon=True)
    cam_thread.start()

    menu_icon.MenuIcon().run()
    