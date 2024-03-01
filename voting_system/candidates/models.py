from django.db import models
from db import db

# Create your models here.
class candidates(models.Model):
    name = models.CharField(max_length=128)
    flag = models.CharField(max_length=128)


candidates_collection = db['candidates']