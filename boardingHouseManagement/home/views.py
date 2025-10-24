from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import logout, login, authenticate
from room.models import Room, Guests

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')


def user_register(request):
    form = UserRegister()
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    return render(request, 'pages/user_register.html', {'form': form})


def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'pages/user_login.html', {'form': form, 'message': 'Tên đăng nhập hoặc mật khẩu không hợp lệ'})
            
    return render(request, 'pages/user_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def rooms_with_guests(request):
    rooms_with_guests = Room.objects.filter(guest__isnull=False)
    return render(request, 'pages/rooms_with_guests.html', {'rooms_with_guests': rooms_with_guests})

def empty_rooms(request):
    empty_rooms = Room.objects.filter(guest__isnull=True)
    return render(request, 'pages/empty_rooms.html', {'empty_rooms': empty_rooms})

