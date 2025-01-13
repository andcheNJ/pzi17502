import cv2
 
# Get and print available backend as dict
print({cv2.videoio_registry.getBackendName(b): b for b in cv2.videoio_registry.getBackends()})
 
cap = cv2.VideoCapture(index=0, apiPreference=cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_SETTINGS, 0)  # Attempt to display settings menu
 
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)  # Disable auto-exposure mode
# cap.set(cv2.CAP_PROP_EXPOSURE, -5)  # Change exposure manually
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)  # Disable autofocus
# cap.set(cv2.CAP_PROP_FOCUS, 250)  # Set focus distance manually
 
cv2.namedWindow("Webcam")
 
img_counter = 0
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Webcam", frame)
 
    key = cv2.waitKey(1)
    if key & 0xFF == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
 
    elif key & 0xFF == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
 
        print("{} written!".format(img_name))
        img_counter += 1
 
cap.release()
 
cv2.destroyAllWindows()