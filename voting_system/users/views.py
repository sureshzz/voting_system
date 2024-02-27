from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import users_collection
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import users


# Create your views here.
def home(request):
  return HttpResponse('hello world')
        
@csrf_exempt
def register(request):
    # if request.method == 'GET':
    #     # Retrieve CSRF token for GET request
    #     csrf_token = get_token(request)
    #     response = JsonResponse({'message': 'CSRF token retrieved successfully'})
    #     response['X-CSRFToken'] = csrf_token  # Add CSRF token to response headers
    #     return response
       
    if request.method == 'POST':
        print(request, request.method)
        # Retrieve data from POST request
        try:
            data = json.loads(request.body)
            print(data)
            username = data.get('username')
            fingerid = data.get('fingerid')
            imageid = data.get('imageid')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Check if required fields are present
        if fingerid is None or imageid is None or username is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create dictionary with user data
        user_data = {'fingerid': fingerid, 'imageid': imageid,'username':username}
        
        # Insert data into MongoDB collection
        users_collection.insert_one(user_data)
        
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    



# Define the authenticate_finger_id function outside of the view function
def authenticate_finger_id(fingerid):
    # Construct a filter based on your data
    print("inside auth")
    print("fingerid:",fingerid)
    filter = {'fingerid': fingerid}

    # Find documents based on the filter
    document = users_collection.find_one(filter)
    print("document :",document)
    

    # Now you can process db_data as needed
    if document:
      username = document.get('username')
    #     # Access the _id field of the document
      object_id = document.get('_id')
      print("Object ID:", object_id)
      fingerid = document.get("fingerid")
      imageid = document.get('imageid')
    #     # user = authenticate(object_id=object_id) 
    #     return dbusername
      # Create a Django user object
      user = users(username=username,fingerid=fingerid,imageid=imageid)
      print(user)
      return user
    else:
        print("No document found with the specified filter.")
        return None
    
@csrf_exempt
def auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            fingerid = data.get('fingerid')
            print(fingerid)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if fingerid is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Move the authentication check inside the POST block
        user = authenticate_finger_id(fingerid)
        print("outside auth")
        print(user)
        if user is None:
            print("hereeeeeeeeee")
            return JsonResponse({'error': 'Authentication failed'}, status=401)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return JsonResponse({'token': str(refresh.access_token)})