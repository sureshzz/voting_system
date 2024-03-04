from django.http import HttpResponse ,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from candidates.models import candidates_collection

# Create your views here.
@csrf_exempt
def cregister(request):   
    if request.method == 'POST':
        data = json.loads(request.body)
        Firstname = data.get('Firstname')
        print(Firstname)
        Middlename = data.get('Middlename')
        Lastname = data.get('Lastname')
        Citizenshipnum = data.get('Citizenshipnum')
        Address = data.get('Address')
        Gender = data.get('Gender')
        Party = data.get('Partyname')
        Image = data.get('imgId')
        print(Image)
        # Check if required fields are present
        if Citizenshipnum is None or Party is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        # Create dictionary with user data
        user_data = {
                    'Firstname': Firstname,
                    'Middlename': Middlename,
                    'Lastname': Lastname,
                    'Citizenshipnum': Citizenshipnum,
                    'Address': Address,
                    'Gender': Gender,
                    'Address': Address,
                    'Party': Party,
                    'Image': Image
                     }
        duplicate = {"Citizenshipnum":Citizenshipnum}
        existingdoc = candidates_collection.find_one(duplicate)
        if existingdoc:
            return JsonResponse({"error":"existing values already existed"})
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

        json_datalist = []

        # Convert ObjectId to string in each document
        for document in document_list:
            document['Firstname'] = str(document['Firstname'])
            document['Middlename'] = str(document['Middlename'])
            document['Lastname'] = str(document['Lastname'])
            document['Citizenshipnum'] = str(document['Citizenshipnum'])
            document['Party'] = str(document['Party'])
            dict_data = {
                "Firstname":document['Firstname'],
                "Middlename":document['Middlename'] ,
                "Lastname":document['Lastname'] ,
                "Citizenshipnum":document['Citizenshipnum'] ,
                "Party":document['Party'],
                "Image":document['Image']
            }
            json_datalist.append(dict_data)
            # print(json_data)

        # Return JSON response with the serialized data
        return JsonResponse(json_datalist, safe=False)
        
    else:
        return JsonResponse({'error': 'cannot get data'}, status=404)
        # Serialize the document list to JSON
        
    
