from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect

# rooms = [
#     {'id':1, 'name': "Let's learn Python"},
#     {'id':2, 'name': "Design with Me"},
#     {'id':3, 'name': "Frontend Developers"},
# ]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, "User does not exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@csrf_protect
def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        profile = {'username': request.POST.get('username'), 'password':request.POST.get('password')}
        
        user = authenticate(request, profile)
        login(request, user)
        # messages.success(request, 'Logged in successfully')
        return redirect('home')
    else:
        messages.error(request, 'Logged in Fail')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)

    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error Occurred Try Again!')
    return render(request, 'base/login_register.html', {'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                Q(name__icontains = q) |
                                Q(description__icontains = q))
    

    topics = Topic.objects.all()
    room_count = rooms.count()

    context= {'rooms':rooms, 'topics': topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        for room in Room.objects.all():

            if request.user != room.host:
                return HttpResponse("You don't have permissions to complete your action")
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if request.user != room.host:
            return HttpResponse("You don't have permissions to complete your action")
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        if request.user != room.host:
            return HttpResponse("You don't have permissions to complete your action")
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
