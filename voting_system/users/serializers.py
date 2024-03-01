# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users_collection
from users.models import users
import jwt
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users_collection
from users.models import users
import face_recognition
import numpy as np


def compare_embeddings(dbembeddings):
    try:
        image1 = face_recognition.load_image_file("image.jpg")
        if image1 is None:
            raise Exception('Error: Unable to read the image "verification_image.jpg"')
        
        unknown_image = face_recognition.load_image_file('image.jpg')
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e:
        print(e)

        # Retrieve the embeddings from the database

        embeddings = []
        embedding = np.array(['embedding'])
        embeddings.append(embedding)

        # Compare the embeddings with others
        for embedding in embeddings:
            # Perform operations with the embedding as needed
            results = face_recognition.compare_faces([embedding], unknown_encoding, tolerance=0.4)
            
            if any(results):
                # Calculate the face distance (smaller distance means better match)
                face_distance = face_recognition.face_distance([embedding], unknown_encoding)[0]

                # Convert face distance to percentage match (adjust as needed)
                percentage_match = max(0, (1 - face_distance) * 100)

                if percentage_match < 70:
                    print("Error", "Face is not matched")
                else:
                    print("Go to the next page") 
def authenticate_finger_id(fingerid):
    print("inside auth")
    filter = {'fingerid': fingerid}
    document = users_collection.find_one(filter)
    print("document :", document)
    if document:
        dbusername = document.get('username')
        dbobject_id = document.get('_id')
        print("Object ID:", dbobject_id)
        dbfingerid = document.get("fingerid")
        dbimageid = document.get('encoding')
        compare_embeddings(dbimageid)
        user = users(fingerid=dbfingerid, imageid=dbimageid, username=dbusername)
        print("user:", user.fingerid)
        return user
    else:
        print("No document found with the specified filter.")
        return None

class UserLoginSerializer(serializers.Serializer):
    fingerid = serializers.IntegerField()
    imageid = serializers.CharField(max_length = 128 * 100)

    def validate(self, attrs):
        fingerid = attrs.get('fingerid')
        imageid = attrs.get('imageid')
        vvuser = authenticate_finger_id(fingerid,imageid)

        if vvuser:
            # refresh = RefreshToken.for_user(vvuser)
            payload = {
                'uid': vvuser.username,
                'role': "voter"
            }
            secretkey = "abc"
            token = jwt.encode(payload,secretkey,algorithm='HS256')
            print("token:",token)
            return token
        else:
            raise serializers.ValidationError("Incorrect credentials")


