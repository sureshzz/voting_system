from django.http import HttpResponse ,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from candidates.models import candidates_collection
import base64
from django.conf import settings
import os

# Create your views here.
@csrf_exempt
def cregister(request):   
    if request.method == 'POST':
        print("cregister")
        # Retrieve data from POST request
        name = request.POST.get('CandidateName')
        print(name)
        # name = "suresh"
        # fingerid = request.POST.get('fingerid')
        flag = request.FILES.get('Image')
        print(flag)
        # print(flag.name)

        # Check if required fields are present
        if name is None or flag is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if flag:
            with open('candidates/cimages/' + flag.name, 'wb') as destination:
                for chunk in flag.chunks():
                    destination.write(chunk)

        # Create dictionary with user data
        user_data = {'name': name, 'flag': flag.name}
        
        # Insert data into MongoDB collection
        candidates_collection.insert_one(user_data)
        
        return JsonResponse({'message': 'candidate registered successfully'}, status=201)
    
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

import json

def cinfo(request):
    if request.method == 'GET':
        # Retrieve all documents from the users collection
        all_documents = candidates_collection.find()

        # Convert documents to a list of dictionaries
        document_list = [document for document in all_documents]
        print(document_list)

        # Convert ObjectId to string in each document
        for document in document_list:
            document['name'] = str(document['name'])
            name = document['name']
            print(name)
            document['flag'] = str(document['flag'])
            imagename= document['flag']
            image_path = os.path.join(settings.BASE_DIR,'candidates','cimages',imagename)
            # if os.path.exists(image_path):
            #     return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            dic_data = {"name":name,"flag":image_base64}
            json_data = json.dumps(dic_data)
            print(json_data)

        # Return JSON response with the serialized data
        return JsonResponse(json_data, safe=False)
        
    else:
        return JsonResponse({'error': 'Image not found'}, status=404)
        # Serialize the document list to JSON
        
    
