from django.db import models
from db import db

# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=128)
    fingerid = models.CharField(max_length=128)
    imageid = models.CharField(max_length=128)
    # uid = models.CharField(max_length=200)
    # Add other fields as neededs needed

class ImageEmbedding(models.Model):
    embedding = models.JSONField()  # Field to store the embedding array
    userid = models.CharField(max_length = 128)

    def __str__(self):
        return f"Embedding for Image {self.id}"

class votes(models.Model):
    username = models.CharField(max_length=128)
    group = models.CharField(max_length=128)
    # Add other fields as neededs needed

class candidates(models.Model):
    name = models.CharField(max_length=128)
    flag = models.CharField(max_length=128)


users_collection = db['users']
embedd_collection = db['Embedd']
votes_collection = db['votes']
candidates_collection = db['candidates']