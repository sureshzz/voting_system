import face_recognition
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import users_collection
from users.models import votes_collection
import jwt
import numpy as np

@csrf_exempt
def auth(request):
    if request.method == 'POST':   
        Citizenshipnum = request.POST.get('Citizenshipnum')
        Fingerid = request.POST.get('Fingerid')
        image_file = request.FILES.get('Imageid')

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

            vfilter = {'Citizenshipnum': Citizenshipnum}
            vdocument = votes_collection.find_one(vfilter)
            if vdocument:
                return JsonResponse({"error": "You have already voted"})
            else:
                result = authenticate_finger_id(Fingerid, unknown_encoding)
                if result.get('token'):
                    return JsonResponse({'message': result.get('message'), 'token': result.get('token')})
                else:
                    return JsonResponse({'error': result.get('error')}, status=401)

        else:
            return JsonResponse({'error': 'No image file provided'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

def authenticate_finger_id(Fingerid, unknown_encoding):
    filter = {'Fingerid': Fingerid}      
    document = users_collection.find_one(filter)
    if document:
        Citizenshipnum = document.get('Citizenshipnum')
        db_encoding = np.array(document.get('Encoding'))
        result = compare_embeddings(db_encoding, unknown_encoding)
        if result:
            payload = {'Citizenshipnum': Citizenshipnum, 'role': "voter"}
            secretkey = "abc"
            token = jwt.encode(payload, secretkey, algorithm='HS256')
            return {'message': 'You are logged in', 'token': token}
        else:
            return {'error': 'Face is not recognized'}
    else:
        return {'error': 'Fingerprint does not match'}

def compare_embeddings(db_encoding, unknown_encoding, tolerance=0.4):
    # Compare the encodings
    result = face_recognition.compare_faces([db_encoding], unknown_encoding, tolerance=tolerance)
    return result[0] if result else False

