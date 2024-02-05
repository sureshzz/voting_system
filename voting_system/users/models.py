from django.db import models
from db import db

# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # Add other fields as neededs needed

class Image(models.Model):
    image_data = models.BinaryField()

users_collection = db['users']