from django.http import HttpResponse ,JsonResponse
from superadmin.models import admin_collection
import json
from django.views.decorators.csrf import csrf_exempt
from candidates.models import candidates_collection

# Create your views here.
@csrf_exempt
def cregister(request):   
    if request.method == 'POST':
        print(request, request.method)
        # Retrieve data from POST request
        try:
            name = request.POST.get('CandidateName')
            # fingerid = request.POST.get('fingerid')
            flag = request.FILES.get('image')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Check if required fields are present
        if name is None or flag is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if flag:
            with open('./' + flag.name, 'wb') as destination:
                for chunk in flag.chunks():
                    destination.write(chunk)

        # Create dictionary with user data
        user_data = {'name': name, 'flag': flag}
        
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
            document['_id'] = str(document['_id'])

        # Serialize the document list to JSON
        json_data = json.dumps(document_list)

        # Return JSON response with the serialized data
        return JsonResponse(json_data, safe=False)