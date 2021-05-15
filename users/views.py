from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rent_app.models import House, HouseImages, Review, Requests
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
import datetime
from django.db import connection
from django.core.mail import send_mail


def emailSender(subject, message, mailID):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mailID, ]
    send_mail( subject, message, email_from, recipient_list )


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_name=request.POST.get('username')

        try:
            CustomUser.objects.get(email=email)
            print('user already exists')
            return redirect('/register')
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                email=email,
                user_name=user_name,
                password=password
            )
            auth.login(request,user)
            
            subject = 'Welcome to Rental Management'
            message = f'Hi {user.user_name}, Thank you for registering on our webiste. If you have any problem accessing it, please contact us.\n\nThank you'
            emailSender(subject, message, user.email)
        
        return redirect('/')
    return render(request, 'register.html')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            subject = 'New sign in to our website'
            message = f'Hi {user.user_name}, Recently you logged in to Rental Webiste management website. If it is not you, please change your password.\nThank you'
            emailSender(subject, message, user.email)
            return redirect('/')
        else:
            # Invalid email or password. Handle as you wish
            return redirect('/')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/login')
def dashboard(request):
    # Here request.user.id gives the id of the user and not the object itself.
    ownedHouses = House.objects.raw("SELECT * FROM rent_app_house where owner_id_id = " + str(request.user.id))
    
    ownedHouseThumbnails = []

    # Fetch all images from house images
    houseImages = HouseImages.objects.raw("SELECT * FROM rent_app_houseimages")
    
    # Just using house.house_id gives house object and not the real ID, so using pk attribute we get the ID
    for house in ownedHouses:
        for image in houseImages:
            if image.house_id.pk == house.pk:
                ownedHouseThumbnails.append([house.pk, image.image])
                break

    # Fetch all reviews of the user
    reviewsGiven = Review.objects.raw("SELECT * FROM rent_app_review where user_id_id = " + str(request.user.id))
    # Data obtained from the queries must be passed to the dashboard.html template
    context = {
        'housesOwned': len(ownedHouses),
        'reviewsGiven': len(reviewsGiven),
        'ownedHouseThumbnails': ownedHouseThumbnails,
        'ownedHouses': ownedHouses
    }
    return render(request, 'dashboard.html', context)



def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
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
