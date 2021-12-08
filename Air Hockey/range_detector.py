import cv2
import numpy as np

def nothing(x):
    pass

# Camera Object
camera = cv2.VideoCapture(0)

camera.set(3,320);
camera.set(4,240);

cv2.namedWindow('Trackbars',0)
cv2.createTrackbar('H_MIN','Trackbars',0,255,nothing)
cv2.createTrackbar('S_MIN','Trackbars',0,255,nothing)
cv2.createTrackbar('V_MIN','Trackbars',0,255,nothing)
cv2.createTrackbar('H_MAX','Trackbars',0,255,nothing)
cv2.createTrackbar('S_MAX','Trackbars',0,255,nothing)
cv2.createTrackbar('V_MAX','Trackbars',0,255,nothing)

while(True):

    # Take each frame
    ret, frame = camera.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get values from track bar
    h_min = cv2.getTrackbarPos('H_MIN','Trackbars')
    s_min = cv2.getTrackbarPos('S_MIN', 'Trackbars')
    v_min = cv2.getTrackbarPos('V_MIN', 'Trackbars')
    h_max = cv2.getTrackbarPos('H_MAX', 'Trackbars')
    s_max = cv2.getTrackbarPos('S_MAX', 'Trackbars')
    v_max = cv2.getTrackbarPos('V_MAX', 'Trackbars')

    # define range of color in HSV
    lower_range = np.array([h_min, s_min, v_min])
    upper_range = np.array([h_max, s_max, v_max])

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Show original frame, and mask
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    # Quit window
    if cv2.waitKey(1) & 0xFF is ord('q'):
        break

camera.release()
cv2.destroyAllWindows()