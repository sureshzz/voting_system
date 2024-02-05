from django.shortcuts import render
from django.http import HttpResponse
from bson import Binary
from PIL import Image
from io import BytesIO

# Create your views here.
def home(request):
  return HttpResponse('hello world')

# def register(request):
  