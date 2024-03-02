from django.http import HttpResponse ,JsonResponse
from users.models import users_collection
from django.views.decorators.csrf import csrf_exempt
import face_recognition
from users.models import users_collection


@csrf_exempt
def register(request):
    if request.method == 'POST':
        Firstname = request.POST.get('Firstname')
        Middlename = request.POST.get('Middlename')
        Lastname = request.POST.get('Lastname')
        Citizenshipnum = request.POST.get('citizenshipnum')
        Address = request.POST.get('Address')
        Date_of_birth = request.POST.get('Date_of_birth')
        Gender = request.POST.get('Gender')
        fingerid = request.POST.get('fingerid')
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
                encoding_dict = {'Firstname': Firstname,
                                 'Middlename': Middlename,
                                 'Lastname': Lastname,
                                 'Citizenshipnum': Citizenshipnum,
                                 'Address': Address,
                                 'Dateofbirth': Date_of_birth,
                                 'Gender': Gender,
                                 'encoding': encoding.tolist(),
                                 'fingerid': fingerid}
                print(encoding_dict)

                users_collection.insert_one(encoding_dict)
            
            return JsonResponse({'title': "done"})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
    
    return JsonResponse({"status": "done"})

        




