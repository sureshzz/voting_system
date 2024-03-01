from django.http import HttpResponse ,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from .models import votes_collection
from users.models import votes_collection



# Create your views here.
def home(request):
  return HttpResponse('hello sohan')

@csrf_exempt
def vote(request):
    # Only authenticated users can access this view due to IsAuthenticated permission
    if request.method == 'POST':
        try:
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
    





        