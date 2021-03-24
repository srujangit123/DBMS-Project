from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,auth
from django.shortcuts import get_object_or_404
from .models import CustomUser,CustomUserManager, House, HouseImages
from django.conf import settings
from .forms import *
from django.contrib import messages


def HomePage(request):
    # print(request.user)

    # select image from houseImages; 
    # houseImagesURL = HouseImages.objects.values_list('image')
    
    # select * from houseImages
    houseImages = HouseImages.objects.all()

    # select * from houses;
    houses = House.objects.all()

    # Contains [house_id, thumbnail_image] array of arrays
    houseThumbnails = []

    # Just using house.house_id gives house object and not the real ID, so using pk attribute we get the ID
    for house in houses:
        for image in houseImages:
            if image.house_id.pk == house.pk:
                houseThumbnails.append([house.pk, image.image])
                break

    for ob in houseThumbnails:
        print(ob[0], ob[1])

    context = {
        'thumbnails' : houseThumbnails,
        'houses': houses
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.user.is_authenticated:
        print(request.user.user_name)
        print(request.user.profile_image)
        return render(request, 'dashboard.html')
    else:
        return redirect('/login')


def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        print("post")
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('/dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    context = {
        'p_form': form
    }
    return render(request, 'update_profile.html', context)