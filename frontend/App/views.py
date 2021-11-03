from django.shortcuts import render
import requests
# Create your views here.

endpoint = 'http://192.168.1.15:5000/'

def home(request):
    respone = requests.get(endpoint+'')
    characters = respone.json()
    context = {
        'characters':characters
    }
    return render(request, 'index.html')