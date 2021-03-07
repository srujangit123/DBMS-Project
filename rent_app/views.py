from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserRegisterForm, UserLoginForm

<<<<<<< HEAD
# Create your views here.
def index(request):
    return render(request, 'rent_app/home.html',{})
=======

def HomePage(request):
    return render(request, 'home.html')


def Register(request):
    next_page = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context = {
        'form': form,
    }
    print(form)
    return render(request, 'register.html', context)


def Login(request):
    next_page = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context = {
        'form': form,
    }
    print(form)
    return render(request, 'login.html', context)


def Logout(request):
    logout(request)
    return render('/')



@login_required
def DashboardPage(request):
    return render(request, 'home.html')
>>>>>>> 17c217a0713a70074804b343f96f27894b69fc30
