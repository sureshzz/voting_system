from django.db import models
from db import db

# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=30, unique=True)
    fingerid = models.CharField(max_length=128)
    imageid = models.CharField(max_length=128)
    # Add other fields as neededs needed


users_collection = db['users']