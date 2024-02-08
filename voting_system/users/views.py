from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from bson import Binary
from PIL import Image
from io import BytesIO
from .models import users_collection
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def home(request):
  return HttpResponse('hello world')


# def register(request):
#   # if request.method == 'POST':
#   # fingerid : request.POST.get(id)
#   # imageid : request.POST.get(image)
#     id : 1 
#     image : 1234
#     user_data = {'id':id,'image': image}
#     users_collection.insert_one(user_data)

    #if request data is not in json
# finger_id = request.POST.get('fingerid')
        # image_id = request.POST.get('imageid')
        # print(finger_id,image_id)
        
@csrf_exempt
def register(request):
    if request.method == 'POST':
        print(request,request.method)
        # Retrieve data from POST request
        try:
            data = json.loads(request.body)
            finger_id = data.get('fingerid')
            image_id = data.get('imageid')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Check if required fields are present
        if finger_id is None or image_id is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create dictionary with user data
        user_data = {'fingerid': finger_id, 'imageid': image_id}
        
        # Insert data into MongoDB collection
        users_collection.insert_one(user_data)
        
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def auth(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      finger_id = data.get('fingerid')


    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    if finger_id is None :
      return JsonResponse({'error': 'Missing required fields'}, status=400)   
    
    db_data = users_collection.find(finger_id)
    print(db_data)