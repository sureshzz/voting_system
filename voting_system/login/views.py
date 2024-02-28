from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import users_collection
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import users
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
def authenticate_finger_id(fingerid):
    # Construct a filter based on your data
    print("inside auth")
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
      # Create a Django user object
      user = users(fingerid=fingerid,imageid=imageid,username=username)
      print("user:",user.fingerid)
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
        if user is None:
            print("hereeeeeeeeee")
            return JsonResponse({'error': 'Authentication failed'}, status=401)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return JsonResponse({'token': str(refresh.access_token)})