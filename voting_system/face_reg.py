import cv2
import face_recognition
from PIL import Image

# Create a video capture object for the front camera
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the camera is opened successfully
if not vid.isOpened():
    print("Could not open video device")
    exit()

# Set the resolution of the camera
vid.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)





# Continuously capture and display the video frames
while True:
    # Capture frame-by-frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    # If the key is 's', save the image and exit the loop
    if key == ord('s'):
        cv2.imwrite('captured_image.jpg', frame)
        break
    # If the key is 'q', exit the loop without saving the image
    elif key == ord('q'):
        break

# Release the video capture object and destroy all windows
vid.release()
cv2.destroyAllWindows()





image= face_recognition.load_image_file("captured_image.jpg")
face_locations = face_recognition.face_locations(image)
# Crop the image based on the first face found
top, right, bottom, left = face_locations[0]
face_image = image[top:bottom, left:right]

# Save or display the cropped face image
pil_image = Image.fromarray(face_image)
pil_image.save('cropped_image.jpg')
