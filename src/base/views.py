from django.shortcuts import render, redirect
from .models import Room 
from .forms import RoomForm

# rooms = [
#     {'id':1, 'name': "Let's learn Python"},
#     {'id':2, 'name': "Design with Me"},
#     {'id':3, 'name': "Frontend Developers"},
# ]

def home(request):
    rooms = Room.objects.all()
    context= {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

