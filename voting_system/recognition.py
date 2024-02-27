import face_recognition
import pymongo
import numpy as np
import os


unknown_image = face_recognition.load_image_file("captured_image1.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]



# Connect to the MongoDB database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['major']
collection = db['embedd']

# Retrieve the embeddings from the database
embeddings = []
for document in collection.find():
    embedding = np.array(document['embedding'])
    embeddings.append(embedding)
   

# Compare the embeddings with others
for embedding in embeddings:
    # Perform operations with the embedding as needed
    results = face_recognition.compare_faces([embedding], unknown_encoding, tolerance=0.4)  # Fix this line
    print(results)
    if any(results):
        # Calculate the face distance (smaller distance means better match)
        face_distance = face_recognition.face_distance([embedding], unknown_encoding)[0]

        # Convert face distance to percentage match (adjust as needed)
        percentage_match = max(0, (1 - face_distance) * 100)

        print(f"Match with embedding  {percentage_match:.2f}% (Face Distance: {face_distance:.4f})")

file = "captured_image1.jpg"
if os.path.exists(file):
    os.remove(file)
else:
    print("The file does not exist")

file1 = "cropped_image1.jpg"
if os.path.exists(file1):
    os.remove(file1)
else:
    print("The file does not exist")
