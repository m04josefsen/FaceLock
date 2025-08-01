import cv2

print("OpenCV version:", cv2.__version__)

# Try accessing webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    cv2.imshow("Webcam Test", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Failed to access webcam.")

cap.release()