from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,auth
from django.shortcuts import get_object_or_404
from .models import CustomUser,CustomUserManager

def HomePage(request):
    print(request.user)
    return render(request, 'home.html')


# def ownerhome(request):
#     if request.user.is_authenticated and user_type.objects.get(user=request.user).is_owner:
#         return render(request, 'owner_home.html')
#     elif request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
#         return redirect('userhome')
#     else:
#         return redirect('login')


# def userhomehome(request):
#     if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
#         return render(request,'user_home.html')
#     elif request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
#         return redirect('ownerhome')
#     else:
#         return redirect('home')


def signup(request):
    if (request.method == 'POST'):
        print(request.POST)
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')
        user_name=request.POST.get('username')
        try:
            CustomUser.objects.get(email=email)
            print('user already exist')
            return redirect('/register')
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                email=email,
                user_name=user_name,
                password=password
            )
            print(user)
            auth.login(request,user)
        return redirect('/')
        print('sign1111')
    return render(request, 'register.html')


def login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        # print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            # Invalid email or password. Handle as you wish
            print('here1')
            return redirect('/')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def dashboard(request):
    return render(request,'dashboard.html')