from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id':1, 'name': "Let's learn Python"},
    {'id':2, 'name': "Design with Me"},
    {'id':3, 'name': "Frontend Developers"},
]

def home(request):
    return render(request, 'home.html', {'rooms':rooms})

def room(request):
    return render(request, 'room.html')

