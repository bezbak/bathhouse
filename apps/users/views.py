from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from apps.sklad.models import Venue
from .models import User
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)
            return redirect('choose_venue')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def choose_venue(request):
    venues = Venue.objects.all()
    if request.method == 'POST':
        vid = request.POST.get('venue_id')
        v = Venue.objects.get(id=vid)
        # здесь можно сохранить выбранное в профиль через user.profile (или cookie)
        request.user.profile.selected_venue_id = v.id
        request.user.profile.save()
        return redirect('dashboard')
    return render(request, 'choose_venue.html', {'venues': venues})

def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Такой пользователь уже существует")
            return redirect("register")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Неверный логин или пароль")
            return redirect("login")
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    return render(request, "dashboard.html")