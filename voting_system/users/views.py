from django.http import HttpResponse ,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from .models import votes_collection
from users.models import votes_collection,users_collection



# Create your views here.
def home(request):
  return HttpResponse('hello broda')

@csrf_exempt
def vote(request):
    # Only authenticated users can access this view due to IsAuthenticated permission
    if request.method == 'POST':
        try:
            received_token = request.headers.get("Authorization")
            parts = received_token.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
        # Handle case where Authorization header is not in the expected format
                return JsonResponse({'error': 'Invalid Authorization header format'}, status="error")

            # Extract the token from the Authorization header
            extracted_token = parts[1]
            print(extracted_token)
            secretkey = "abc"
            decoded_token = jwt.decode(extracted_token,secretkey,algorithms=['HS256'])
            # actual_token = decoded_token.split(' ')[1]
            print("decoded_token:",decoded_token)
            validater = decoded_token['role']
            Citizenshipnum = decoded_token['Citizenshipnum']
            print(validater)
            data = json.loads(request.body)
            Party = data.get('Party')
            Date = data.get('Date')
            Candidatenum = data.get('Candidatecitizenshipnum')
            Candidatename = data.get('Candidatename')
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON data'}, status=400)
        
        if Party is None or Candidatename is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        if validater == 'voter':
        # Proceed with your vote logic using the authenticated user (request.user)
            dict ={
                'Party':Party,
                'Citizenshipnum':Citizenshipnum,
                'Candidatename':Candidatename,
                'Candidatenum':Candidatenum
            }
            result = votes_collection.insert_one(dict)
            print(result)
            return JsonResponse({"status": "200"})

def votecount(request):
    if request.method == 'GET':
        try:
            # Total voters aggregation
            total_voters = list(users_collection.objects.aggregate([
                {
                    '$facet': {
                        'pipeline1': [
                            {'$group': {'_id': '$Citizenshipnum', 'totalvoters': {'$sum': 1}}}
                        ],
                        # Add more pipelines for Model1 as needed
                    }
                }
            ]))

            # Today's votes aggregation
            today_votes = list(votes_collection.objects.aggregate([
                {
                    '$facet': {
                        'pipeline2': [
                            {'$group': {'_id': '$Date', 'todayvotes': {'$sum': 1}}}
                        ],
                        # Add more pipelines for Model1 as needed
                    }
                }
            ]))

            # Party-wise votes aggregation
            pipeline = [
                {"$group": {"_id": "$Party", "votesperparty": {"$sum": 1}}}
            ]
            party_votes = list(votes_collection.aggregate(pipeline))

            return JsonResponse({
                "total_voters": total_voters,
                "today_votes": today_votes,
                "party_votes": party_votes
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)






        