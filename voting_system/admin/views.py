from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from models import admin_collection
import json
from django.views.decorators.csrf import csrf_exempt
import jwt
from users.models import candidates_collection

# Create your views here.
@csrf_exempt
def deletecandidate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        filter = {'name': name}
        result = candidates_collection.delete_one(filter)

        if result.deleted_count == 1:
            return JsonResponse({'message': 'Document deleted successfully.'})
        else:
            return JsonResponse({'error': 'Document not found or could not be deleted.'}, status=404)
    else:
        return JsonResponse({'error': 'Task is not supported'}, status=405)
    

from django.http import JsonResponse

@csrf_exempt
def adminlogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        filter = {"username": username}
        document = admin_collection.find_one(filter)

        if document:
            if document.get('password') == password:
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