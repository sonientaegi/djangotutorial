from django import http
from django.shortcuts import render

# Create your views here.
def index(request):
    return http.HttpResponse("Hello, world. You're at the polls index.")