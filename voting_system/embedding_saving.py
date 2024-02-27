import os
import cv2
import face_recognition
from pymongo import MongoClient
from PIL import Image



image= face_recognition.load_image_file("captured_image.jpg")

if image is not None:
   
    known_image = face_recognition.load_image_file('captured_image.jpg')
    known_encoding = face_recognition.face_encodings(known_image)[0]
else:

    print(f'Error: Unable to read the image {image}')

known_encoding_list = known_encoding.tolist()

# Create a connection
client = MongoClient('localhost', 27017)

# Accessing a database
db = client['majordb']

# Accessing a collection
collection = db['embedd']

#known_encoding1=face_landmarks_list.tolist()
document = {
    'embedding':known_encoding_list
    
}
result = collection.insert_one(document)

# Print the unique identifier for the inserted document
print(result.inserted_id)

# Close the connection
client.close()

file = "captured_image.jpg"
if os.path.exists(file):
    os.remove(file)
else:
    print("The file does not exist")

file1 = "cropped_image.jpg"
if os.path.exists(file1):
    os.remove(file1)
else:
    print("The file does not exist")


