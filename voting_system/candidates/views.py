from django.http import HttpResponse ,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from candidates.models import candidates_collection

# Create your views here.
@csrf_exempt
def cregister(request):   
    if request.method == 'POST':
        Firstname = request.POST.get('Firstname')
        Middlename = request.POST.get('Middlename')
        Citizenshipnum = request.POST.get('Citizenshipnum')
        Address = request.POST.get('Address')
        Gender = request.POST.get('Gender')
        Party = request.POST.get('Party')
        # Check if required fields are present
        if Citizenshipnum is None or Party is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        # Create dictionary with user data
        user_data = {
                    'Firstname': Firstname,
                    'Middlename': Middlename,
                    'Citizenshipnum': Citizenshipnum,
                    'Address': Address,
                    'Gender': Gender,
                    'Address': Address,
                    'Party': Party
                     }
        duplicate = {"Citizenshipnum":Citizenshipnum}
        existingdoc = candidates_collection.find_one(duplicate)
        if existingdoc:
            return JsonResponse("existing values already existed")
        else:    
            candidates_collection.insert_one(user_data)
            
            return JsonResponse({'message': 'candidate registered successfully'}, status=201)
    
    else:
        return JsonResponse({'error': 'candidate couldnot be registered'}, status=405)
    

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
            document['Firstname'] = str(document['Firstname'])
            document['Middlename'] = str(document['Middlename'])
            document['Lastname'] = str(document['Lastname'])
            document['Party'] = str(document['Party'])
            dict_data = {
                "Firstname":document['Firstname'],
                "Middlename":document['Middlename'] ,
                "Lastname":document['Lastname'] ,
                "Party":document['Party']
            }
            json_data = json.dumps(dict_data)
            print(json_data)

        # Return JSON response with the serialized data
        return JsonResponse(json_data, safe=False)
        
    else:
        return JsonResponse({'error': 'cannot get data'}, status=404)
        # Serialize the document list to JSON
        
    
