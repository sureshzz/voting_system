from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from users.models import users_collection
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import users
import numpy as np
from PIL import Image
from io import BytesIO
from face_recognition import face_encodings

        
# def save_embedding(image_data):
#     try:
#         image = image_data
#         image_binary = base64.b64decode(image_data)
#     #storing embeds
#         result = embedd_collection.insert_one({"image":image_binary})
#         if result.inserted_id:
#             return JsonResponse({'message': 'Image encoding saved successfully',}, status=201),image_binary
#         else:
#             return JsonResponse({'error': 'Failed to save image encoding'}, status=500)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

def generate_face_embeddings(image_data):
    # Convert image data to numpy array
    image_np = np.array(Image.open(image_data))
    
    # Generate face embeddings
    face_embeddings = face_encodings(image_np)
    print(face_embeddings)
    return face_embeddings

@csrf_exempt
def register(request):
    if request.method == 'POST':
        print(request, request.method)
        # Retrieve data from POST reques
        try:
            data = json.loads(request.body)
            username = data.get('username')
            fingerid = data.get('fingerid')
            imageid = data.get('imageid')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Check if required fields are present
        if fingerid is None or imageid is None or username is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)   
        image_data = imageid
        # Generate face embeddings
        face_embeddings = generate_face_embeddings(image_data)

        # Create dictionary with user data
        user_data = {'fingerid': fingerid, 'imageid': face_embeddings,'username':username}
        
        # Insert data into MongoDB collection
        users_collection.insert_one(user_data)
            
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

