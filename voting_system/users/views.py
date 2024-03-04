from django.http import HttpResponse ,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from .models import votes_collection
from users.models import votes_collection,users_collection
from candidates.models import candidates_collection



# Create your views here.
def home(request):
  return HttpResponse('hello broda')


from datetime import datetime

@csrf_exempt
def vote(request):
    # Get the current time
    # current_time = datetime.now().time()

    # Check if the current time is within the allowed hours (11am to 5pm)
    # if current_time >= datetime.strptime('11:00', '%H:%M').time() and \
    #         current_time <= datetime.strptime('23:00', '%H:%M').time():
        # API logic
        # Only authenticated users can access this view due to IsAuthenticated permission
    if request.method == 'POST':
            try:
                received_token = request.headers.get("Authorization")
                parts = received_token.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    # Handle case where Authorization header is not in the expected format
                    return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

                # Extract the token from the Authorization header
                extracted_token = parts[1]
                print(extracted_token)
                secretkey = "abc"
                decoded_token = jwt.decode(extracted_token, secretkey, algorithms=['HS256'])
                print("decoded_token:", decoded_token)
                validater = decoded_token['role']
                Citizenshipnum = decoded_token['Citizenshipnum']
                print(validater)
                data = json.loads(request.body)
                Party = data.get('Party')
                Date = data.get('Date')
                print(Date)
                Candidatenum = data.get('Candidatecitizenshipnum')
                Candidatename = data.get('Candidatename')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

            if Party is None or Candidatename is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            duplicate = {"Citizenshipnum": Citizenshipnum}
            existingdoc = votes_collection.find_one(duplicate)
            if existingdoc:
                return JsonResponse("existing values already existed")
            else:
                if validater == 'voter':
                    # Proceed with your vote logic using the authenticated user (request.user)
                    dict = {
                        'Party': Party,
                        'Citizenshipnum': Citizenshipnum,
                        'Candidatename': Candidatename,
                        'Candidatenum': Candidatenum,
                        'Date': Date
                    }
                    result = votes_collection.insert_one(dict)
                    print(result)
                    return JsonResponse({"status": "200"})
    else:
        return JsonResponse({"error":"try again"})
    # else:
    #     # Return an error message if the API is accessed outside the allowed hours
    #     return JsonResponse({'error': 'API is only available between 11am and 5pm'}, status=403)


from datetime import datetime

def votecount(request):
    if request.method == 'GET':
        try:
            # Get today's date
            Date = datetime.today().date()
            date_str = Date.strftime("%Y-%m-%d")

            # Total voters and candidates count
            total_voters = users_collection.count_documents({})
            total_candidates = candidates_collection.count_documents({})

            # Today's votes aggregation
            pipeline1 = [
                {"$match": {"Date": date_str}},  # Filter by today's date
                {"$group": {"_id": "$Date", "count": {"$sum": 1}}}
            ]
            today_votes_cursor = votes_collection.aggregate(pipeline1)
            today_votes_list = list(today_votes_cursor)  # Convert cursor to list of documents

            # Party-wise votes aggregation
            pipeline2 = [
                {"$group": {"_id": "$Party", "votesperparty": {"$sum": 1}}}
            ]
            party_votes = list(votes_collection.aggregate(pipeline2))

            return JsonResponse({
                "totalvoters": total_voters,
                "totalcandidates": total_candidates,
                "todayvotes": today_votes_list,  # Use the list of documents
                "partyvotes": party_votes
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)





# from django.http import JsonResponse
# from datetime import datetime
# from bson import ObjectId  # Import ObjectId to convert MongoDB ObjectId to string

# def votecount(request):
#     if request.method == 'GET':
#         try:
#             # Get today's date
#             today_date = datetime.today().date()
#             date_str = today_date.strftime("%Y-%m-%d")

#             # Aggregate pipeline to calculate total count of documents in votes_collection grouped by party
#             pipeline2 = [
#     # Lookup stage to perform a left outer join with votes_collection
#     {
#         "$lookup": {
#             "from": "votes_collection",
#             "localField": "Party",
#             "foreignField": "Party",
#             "as": "votes"
#         }
#     },
#     # Project stage to handle cases where there are no matching documents in votes_collection
#     {
#         "$project": {
#             "Party": 1,  # Preserve the Party field
#             "votes_count": {
#                 "$cond": {
#                     "if": {"$eq": [{"$size": "$votes"}, 0]},  # Check if votes array is empty
#                     "then": 0,  # If empty, set votes_count to 0
#                     "else": {"$size": "$votes"}  # Otherwise, count the number of elements in votes array
#                 }
#             }
#         }
#     }
# ]

#             party_votes = list(candidates_collection.aggregate(pipeline2))

#             print(party_votes)

#             # Convert ObjectId to string for Party field
#             for vote in party_votes:
#                 vote["_id"] = str(vote["_id"])

#             return JsonResponse({
#                 "party_votes": party_votes
#             })

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)








        