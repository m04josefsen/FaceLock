# FaceLock

> Python application to lock your MacBook when leaving the frame

## Requirments
- macOS
- Python 3.8 or newer

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/FaceLock.git
cd FaceLock
```

### 2. Create and activate a virtual environment (optional)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

## Usage
1. If you are using facial recognition, place an image of your face inside face_lock/
Make sure the naming is correct in load_facial_recognition() in face_lock.py
2. Run the app
```bash
python main.py
```
3. Choose whether or not to use facial recognition, and the amount of seconds before screen locks

Make sure Terminal or your Python app has permissions to control the display (System Settings > Privacy & Security > Accessibility).

## Configuration
- Camera Index: If the webcam doesn’t work, change the camera_index variable in face_lock.py (usually 0 or 1). 0 is usually your iPhone if "continuity camera" is turned on

![FaceLock](https://github.com/user-attachments/assets/457ba656-152b-4b5c-b8d5-2a2cb6ae84f0)
