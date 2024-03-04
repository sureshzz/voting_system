from django.db import models
from db import db

# Create your models here.

class users(models.Model):
    Firstname = models.CharField(max_length=128)
    Middlename = models.CharField(max_length=128)
    Lastname = models.CharField(max_length=128)
    Citizenshipnum = models.CharField(max_length=128)
    Address = models.CharField(max_length=128)
    Date_of_birth = models.CharField(max_length=128)
    Gender = models.CharField(max_length=128)
    Fingerid = models.IntegerField()
    Imageid = models.CharField(max_length=128 * 100)

class votes(models.Model):
    Voterid = models.CharField(max_length = 128)
    Candidateid = models.CharField(max_length = 128)
    Date = models.CharField(max_length=128)
    Group = models.CharField(max_length=128)
    Candidatename = models.CharField(max_length=128)
    # Add other fields as neededs needed






users_collection = db['users']
votes_collection = db['votes']

