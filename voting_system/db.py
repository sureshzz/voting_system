import pymongo

url = "mongodb+srv://sureshthapamagar8914:43Kg9rFNlQuyZRHb@cluster0.69fzi09.mongodb.net/"
client = pymongo.MongoClient(url)

db = client['majordb']