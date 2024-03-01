from django.db import models
from db import db

# Create your models here.
class admin(models.Model):
    name = models.CharField(max_length = 128)
    password = models.CharField(max_length = 128)


admin_collection = db['admin']