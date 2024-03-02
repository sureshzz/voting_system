import face_recognition
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import users_collection
import jwt
import numpy as np

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

            if not face_encodings:
                return JsonResponse({'error': 'No faces found in the image'}, status=400)

            unknown_encoding = face_encodings[0]  # Assuming only one face is detected

            # Define the authenticate_finger_id function
            def authenticate_finger_id(fingerid):
                filter = {'fingerid': fingerid}
                document = users_collection.find_one(filter)
                if document:
                    db_embedding = np.array(document.get('encoding'))
                    result = compare_embeddings(db_embedding, unknown_encoding)
                    if result:
                        payload = {'username': username, 'role': "voter"}
                        secretkey = "abc"
                        token = jwt.encode(payload, secretkey, algorithm='HS256')
                        return token
                    else:
                        return None
                else:
                    print("No document found with the specified filter.")
                    return None

            # Call the authenticate_finger_id function
            result = authenticate_finger_id(fingerid)

            if result:
                return JsonResponse({'token': result})
            else:
                return JsonResponse({'error': 'Authentication failed'}, status=401)

        else:
            return JsonResponse({'error': 'No image file provided'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

def compare_embeddings(db_embedding, unknown_encoding, tolerance=0.4):
    # Compare the embeddings with others
    result = face_recognition.compare_faces([db_embedding], unknown_encoding, tolerance=tolerance)
    return result[0] if result else False
