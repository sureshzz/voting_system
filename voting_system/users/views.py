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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
import jwt
from .models import votes_collection
from .models import candidates_collection


# Create your views here.
def home(request):
  return HttpResponse('hello sohan')
        
# @csrf_exempt
# def register(request):
#     # if request.method == 'GET':
#     #     # Retrieve CSRF token for GET request
#     #     csrf_token = get_token(request)
#     #     response = JsonResponse({'message': 'CSRF token retrieved successfully'})
#     #     response['X-CSRFToken'] = csrf_token  # Add CSRF token to response headers
#     #     return response
       
#     if request.method == 'POST':
#         print(request, request.method)
#         # Retrieve data from POST request
#         try:
#             data = json.loads(request.body)
#             print(data)
#             username = data.get('username')
#             fingerid = data.get('fingerid')
#             imageid = data.get('imageid')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#         # Check if required fields are present
#         if fingerid is None or imageid is None or username is None:
#             return JsonResponse({'error': 'Missing required fields'}, status=400)
        
#         # Create dictionary with user data
#         user_data = {'fingerid': fingerid, 'imageid': imageid,'username':username}
        
#         # Insert data into MongoDB collection
#         users_collection.insert_one(user_data)
        
#         return JsonResponse({'message': 'User registered successfully'}, status=201)
    
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    



# Define the authenticate_finger_id function outside of the view funct
    
# @csrf_exempt
# def auth(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data)
#             fingerid = data.get('fingerid')
#             print(fingerid)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#         if fingerid is None:
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         # Move the authentication check inside the POST block
#         user = authenticate_finger_id(fingerid)
#         print("outside auth")
#         if user is None:
#             print("hereeeeeeeeee")
#             return JsonResponse({'error': 'Authentication failed'}, status=401)

#         # Generate JWT token
#         payload = {
#             'username':user.username,
#             'fingerid':user.fingerid,
#             'imageid':user.imageid  
#         }
#
@csrf_exempt
@api_view(['POST'])
def auth(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def vote(request):
    # Only authenticated users can access this view due to IsAuthenticated permission
    if request.method == 'POST':
        try:
            # headers = request.headers
            # print(headers)
            received_token = request.headers.get("token")
            print(received_token)
            secretkey = "abc"
            decoded_token = jwt.decode(received_token,secretkey,algorithms=['HS256'])
            # actual_token = decoded_token.split(' ')[1]
            print("decoded_token:",decoded_token)
            validater = decoded_token['role']
            print(validater)
            data = json.loads(request.body)
            group = data.get('group')
            username = data.get('username')
            candidate_name = data.get('candidate_name')
            print(username)
            print(group)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON data'}, status=400)
        
        if group is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        if validater == 'voter':
        # Proceed with your vote logic using the authenticated user (request.user)
            dict ={
                'group':group,
                'userame':username,
                'candidate_name':candidate_name
            }
            result = votes_collection.insert_one(dict)
            print(result)
            return JsonResponse({"status": "200"})

@csrf_exempt
def cregister(request):   
    if request.method == 'POST':
        print(request, request.method)
        # Retrieve data from POST request
        try:
            data = json.loads(request.body)
            print(data)
            name = data.get('name')
            flag = data.get('flag')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Check if required fields are present
        if name is None or flag is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
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
    

def votecount(request):
    if request.method == 'GET':
        
        # Define the aggregation pipeline
        pipeline = [
            {"$group": {"_id": "$group", "total_votes": {"$sum": 1}}}
        ]

        # Execute the aggregation pipeline
        result = list(votes_collection.aggregate(pipeline)) 
        print(result)
        count = json.dumps(result)
        print(count)
        return JsonResponse({"count": count})
    else:
        return HttpResponse("invalid request")
    