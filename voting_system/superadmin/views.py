from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from superadmin.models import admin_collection
import json
from django.views.decorators.csrf import csrf_exempt
import jwt
from candidates.models import candidates_collection
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
def adminsignup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            return JsonResponse({'error': "missing field"}, status=400) 
        hashedpassword = make_password(password)
        data = {
            'username': username,
            'password': hashedpassword
        }
        filter = {"username":username}
        existingdoc = admin_collection.find_one(filter)
        print(existingdoc)
        if existingdoc:
            return JsonResponse({"error":"existing values already existed"})
        else:
            result = admin_collection.insert_one(data)

            if result:
                return JsonResponse({'message': "admin is registered successfully"})  
            else:
                return JsonResponse({'error': "admin registration failed"}, status=500)  

    else:
        return JsonResponse({'error': "invalid request"}, status=400)   

@csrf_exempt
def adminlogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        filter = {"username": username}
        document = admin_collection.find_one(filter)
        dbpassword = document.get('password')

        if document:
            authenticate = check_password(password,dbpassword)#return boolean value so
            if authenticate:
                payload = {
                        "username": username,
                        "role": "admin"
                    }
                token = jwt.encode(payload, "suresh", algorithm='HS256')
                    # Return a JSON response with the token
                return JsonResponse({"token": token})
            else:
                return JsonResponse({"error": "Password is not correct"}, status=400)
        else:
                return JsonResponse({"error": "Invalid inputs, try again"}, status=400)

        # Return a 405 Method Not Allowed response if the request method is not POST
    return JsonResponse({"error": "Method Not Allowed"}, status=405)

# Create your views here.
@csrf_exempt
def deletecandidate(request):
    if request.method == 'POST':
        received_token = request.headers.get('token')
        decoded_token = jwt.decode(received_token,'suresh',algorithms=['HS256'])
        validater = decoded_token['role']
        data = json.loads(request.body)
        name = data.get('name')
        filter = {'name': name}
        if validater == 'admin':
            result = candidates_collection.delete_one(filter)
            return JsonResponse("done")

        if result.deleted_count == 1:
            return JsonResponse({'message': 'Document deleted successfully.'})
        else:
            return JsonResponse({'error': 'Document not found or could not be deleted.'}, status=404)
    else:
        return JsonResponse({'error': 'Task is not supported'}, status=405)
    
@csrf_exempt
def updatecandidate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('candidateid')
        candidate_name = data.get('name')
        flag = data.get('flag')

        filter= {"id":id}

        update = {
            "$set": {
                "field_to_update": candidate_name,
                  "flag" :flag  # Replace with the field and new value to update
            }
        }

        result =  candidates_collection.update_one(filter,update)
        
                # Check if the document was successfully updated
        if result.modified_count == 1:
            print("Document updated successfully.")
        else:
            print("No matching document found or document was not updated.")
    else:
        return JsonResponse ({"cannot update candidate"})
                 
                 
            


    

