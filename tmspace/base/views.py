from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.
def index(request):
    context = {}
    return render(request, 'base\index.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, "base\home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, "base\Room.html", context)

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "base\Room_form.html", context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "base\Room_form.html", context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.method =='POST':
        room.delete()
        return redirect('home')

    return render(request, "base\delete.html", context)

def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username exists.")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email exists.")
            return redirect('signup')

        if pass2 != pass1:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.phone_number = phone
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        messages.success(request, 'Your account has successfully been created.')

        return redirect('signin')
    context = {}
    return render(request, 'base\signup.html', context)

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            context = {'fname':fname}
            return render(request, 'base\home.html', context)

        else :
            messages.error(request, "Check your login info!!")
            return redirect('signin')

    return render(request, 'base\signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'You logged out successfully')
    return redirect('index')