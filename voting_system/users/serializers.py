# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users_collection
from users.models import users
import jwt
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users_collection
from users.models import users

def authenticate_finger_id(fingerid):
    print("inside auth")
    filter = {'fingerid': fingerid}
    document = users_collection.find_one(filter)
    print("document :", document)
    if document:
        dbusername = document.get('username')
        dbobject_id = document.get('_id')
        print("Object ID:", dbobject_id)
        dbfingerid = document.get("fingerid")
        dbimageid = document.get('imageid')
        user = users(fingerid=dbfingerid, imageid=dbimageid, username=dbusername)
        print("user:", user.fingerid)
        return user
    else:
        print("No document found with the specified filter.")
        return None

class UserLoginSerializer(serializers.Serializer):
    fingerid = serializers.CharField()

    def validate(self, attrs):
        fingerid = attrs.get('fingerid')
        vvuser = authenticate_finger_id(fingerid)

        if vvuser:
            # refresh = RefreshToken.for_user(vvuser)
            payload = {
                'uid': vvuser.username,
                'role': "voter"
            }
            secretkey = "abc"
            token = jwt.encode(payload,secretkey,algorithm='HS256')
            print("token:",token)
            return token
        else:
            raise serializers.ValidationError("Incorrect credentials")


