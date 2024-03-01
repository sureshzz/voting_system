import face_recognition
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import users_collection
import numpy as np
import jwt

def compare_embeddings(dbembedding):
    try:
        secimage = face_recognition.load_image_file("image.jpg")
        if secimage is None:
            raise Exception('Error: Unable to read the image "verification_image.jpg"')

        unknown_image = face_recognition.load_image_file('image.jpg')
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e:
        print(e)

    # Retrieve the embeddings from the database
    embeddings = dbembedding
    embedding = np.array([embeddings])

    # Compare the embeddings with others
    results = face_recognition.compare_faces([embedding], unknown_encoding, tolerance=0.4)
    print("results",results)

    if (results[0] == True):
    # if any(element == True for element in results):
        # Calculate the face distance (smaller distance means better match)
        face_distance = face_recognition.face_distance([embedding], unknown_encoding)[0]
        print(face_distance)

        # Convert face distance to percentage match (adjust as needed)
        percentage_match = max(0, (1 - face_distance) * 100)
        print(percentage_match)

        if percentage_match < 70:
            print("Error", "Face is not matched")
        else:
            return "true"

@csrf_exempt
def auth(request):
    if request.method == 'POST':   
        username = request.POST.get('votingdata')
        fingerid = request.POST.get('fingerid')
        image_file = request.FILES.get('imageid')

        if image_file:
            with open('./' + image_file.name, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Load the uploaded image file
            image = face_recognition.load_image_file('./' + image_file.name)

            # Detect faces in the image and get facial encodings
            face_encodings = face_recognition.face_encodings(image)
            print(face_encodings)

            if not face_encodings:
                return JsonResponse({'error': 'No faces found in the image'}, status=400)
            
        #      embeddings = []
        # for document in collection.find():
        #     embedding = np.array(document['embedding'])
        #     embeddings.append(embedding)


            
            # Define the authenticate_finger_id function
            def authenticate_finger_id(fingerid):
                print("inside auth")
                filter = {'fingerid': fingerid}
                document = users_collection.find_one(filter)
                print("document :", document)
                if document:
                    dbobject_id = document.get('_id')
                    print("Object ID:", dbobject_id)
                    dbfingerid = document.get("fingerid")
                    dbembedding = document.get('encoding')
                    # dbembedding = np.array(dbembedding)
                    # print(dbembedding)
                    result = compare_embeddings(dbembedding)  # Assuming compare_embeddings function is defined elsewhere
                    if result == "true":
                        payload = {
                            'uid': username,
                            'role': "voter"
                        }
                        secretkey = "abc"
                        token = jwt.encode(payload, secretkey, algorithm='HS256')
                        print("token:", token)
                        return token

                else:
                    print("No document found with the specified filter.")
                    return None
                # Call the authenticate_finger_id function
            authenticate_finger_id(fingerid)

            return JsonResponse({'title': "done"})

        else:
            return JsonResponse({'error': 'No image file provided'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)