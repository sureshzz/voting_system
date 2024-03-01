from django.http import HttpResponse ,JsonResponse
from users.models import users_collection
from django.views.decorators.csrf import csrf_exempt
import face_recognition


@csrf_exempt
def register(request):
    if request.method == 'POST':
        fingerid = request.POST.get('fingerid')
        content = request.POST.get('FirstName')
        # print(content.FirstName)
        print(content)
        print("hello")
        image_file = request.FILES.get('imageid')
        print("image_file", image_file)
        
        # Handle the uploaded image file
        # For example, save it to a location on your server
        if image_file:
            with open('./' + image_file.name, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Load the uploaded image file
            image = face_recognition.load_image_file("image.jpg")
            print(image)

            # Detect faces in the image and get facial encodings
            face_encodings = face_recognition.face_encodings(image)
            print(face_encodings)
            if not face_encodings:
                # If no faces are detected, return an error response
                return JsonResponse({'error': 'No faces found in the image'}, status=400)
            
            
            # Insert each face encoding into the MongoDB collection
            for encoding in face_encodings:
                encoding_dict = {'encoding': encoding.tolist(),'fingerid': fingerid}
                print(encoding_dict)

                users_collection.insert_one(encoding_dict)
            
            return JsonResponse({'title': "done"})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
    
    return JsonResponse({"status": "done"})

        
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

# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         print(request, request.method)
#         # Retrieve data from POST reques
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             fingerid = data.get('fingerid')
#             imageid = data.get('imageid')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#         # Check if required fields are present
#         if fingerid is None or imageid is None or username is None:
#             return JsonResponse({'error': 'Missing required fields'}, status=400)  
#         print(imageid) 
#         image_data = imageid
#         with open('./image.jpg', 'wb') as f:
#             for chunk in imageid.chunks():
#                 f.write(chunk)
#         # Generate face embeddings
#         face_embeddings = generate_face_embeddings(image_data)

#         # Create dictionary with user data
#         user_data = {'fingerid': fingerid, 'imageid': face_embeddings,'username':username}
        
#         # Insert data into MongoDB collection
#         users_collection.insert_one(user_data)
            
#         return JsonResponse({'message': 'User registered successfully'}, status=201)
    
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



