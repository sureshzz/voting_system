from django.db import models
from db import db

# Create your models here.
class candidates(models.Model):
    Firstname = models.CharField(max_length=128)
    Middlename = models.CharField(max_length=128)
    Citizenshipnum = models.CharField(max_length=128)
    Address = models.CharField(max_length=128)
    Gender = models.CharField(max_length=128)
    Party = models.CharField(max_length=128)
    Image = models.CharField(max_length=128)


candidates_collection = db['candidates']