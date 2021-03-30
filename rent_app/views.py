from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import get_object_or_404
from .models import CustomUser, CustomUserManager, House, HouseImages, Review, Requests
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
import datetime
from django.db import connection


def emailSender(subject, message, mailID):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mailID, ]
    send_mail( subject, message, email_from, recipient_list )

def HomePage(request):
    city = ''
    price = 0
    # city = request.GET['city']
    # print(city)
    
    try:
        # Todo -> filters
        city = request.GET['city']
        price = request.GET['price']
        houses = House.objects.raw("SELECT * FROM rent_app_house where vacant = 1")
        query = "SELECT * FROM rent_app_house where vacant = 1"

        # Price filter
        if price:
            query += " and rent <= " + str(price)

        # city filter
        if city:
            # check for city in uppercase form and lowercase form also
            citylower = city.lower()
            cityupper = city.upper()
            query += " and city = " + f"'{city}'" + " or city = " + f"'{citylower}'" + " or city = " + f"'{cityupper}'"
        print(query)
        houses = House.objects.raw(query)

        if not len(houses):
            messages.success(request, 'No houses  found')
            houses = House.objects.raw("SELECT * FROM rent_app_house where vacant = 1")
            # return render(request,'home.html')
    except:
        print('no city param')
        # select all houses in the house table;
        houses = House.objects.raw("SELECT * FROM rent_app_house where vacant = 1")
    
    # select all house images
    houseImages = HouseImages.objects.raw("SELECT * FROM rent_app_houseimages")

    # # select all houses in the house table;
    # houses = House.objects.raw("SELECT * FROM rent_app_house where vacant = 1")

    # Contains [house_id, thumbnail_image] array of arrays
    houseThumbnails = []

    # Just using house.house_id gives house object and not the real ID, so using pk attribute we get the ID
    for house in houses:
        for image in houseImages:
            if image.house_id.pk == house.pk:
                houseThumbnails.append([house.pk, image.image])
                break


    context = {
        'thumbnails' : houseThumbnails,
        'houses': houses
    }

    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')



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


@login_required(login_url='/login')
def viewHouse(request, house_id):

    # There exists only a single house with this house id ie the first element of the queryset always.
    house = House.objects.raw("SELECT * FROM rent_app_house where house_id = " + str(house_id))[0]
    if house.vacant == 0:
        if request.user.id == house.owner_id.pk:
            messages.error(request, "This house is already rented by a user")
        else:
            if house.rented_id != request.user.id:
                return HttpResponse("This page doesn't exist")
            else:
                messages.success(request, "You are currently renting this house")


    # Fetch all images for the house with given house id
    houseImages = HouseImages.objects.raw("SELECT * FROM rent_app_houseimages where house_id_id = " + str(house_id))

    # Fetch all reviews for the house with given house id
    reviews = Review.objects.raw("SELECT * FROM rent_app_review where house_id_id = " + str(house_id))

    # Data obtained from the queries must be passed to the house_details.html template
    
    # print(house.owner_id.pk)
    # Here we need to pass owner object. Using house.owner_id_id or house.owner_id.pk gives the id number and not the object

    rentRequests = None
    if request.user.id == house.owner_id.pk:
        rentRequests = Requests.objects.raw('SELECT id, user_id_id FROM rent_app_requests where house_id_id = ' + str(house_id))

    isUserAuthorizedToLeave = False

    if house.vacant == 0 and house.rented_id == request.user.id:
        isUserAuthorizedToLeave = True

    context = {
        'house': house,
        'images': houseImages,
        'owner': house.owner_id,
        'reviews': reviews,
        'canLeave': isUserAuthorizedToLeave,
        'requests': rentRequests
    }
    return render(request, 'house_details.html', context)


def addHouse(request):
    # check if user is logged in
    if request.user.is_authenticated:
        if request.method == 'POST':

            # fetch user object
            user = request.user

            # Insert a new record in the house table
            new_house = House.objects.create(owner_id=user,
                                    city=request.POST['city'],
                                    state=request.POST['state'],
                                    address=request.POST['address'],
                                    description=request.POST['description'],
                                    rent=request.POST['rent']
                                    )
            imgs = request.FILES.getlist('image',False)
            for img in imgs:
                if img:
                    imgx = HouseImages(image=img, house_id=new_house)
                    imgx.save()

            return redirect('/houses/' + str(new_house.house_id))
        return render(request,'add_house.html')
    else:
        return redirect("/login")


@login_required(login_url='/login')
def sendRentRequest(request, house_id):
    
    house = House.objects.raw("SELECT * FROM rent_app_house where house_id = " + str(house_id))[0]

    if house.owner_id.pk == request.user.id:
        messages.error(request, 'You are the owner!')
        return redirect('/houses/' + str(house_id))

    rentRequest = Requests.objects.raw('SELECT * FROM rent_app_requests where house_id_id = ' + str(house_id) + ' and user_id_id = ' + str(request.user.id))

    if len(rentRequest) != 0:
        messages.success(request, 'Request already sent')
        return redirect('/houses/' + str(house_id))
    else:
        Requests.objects.create(house_id_id=house_id, user_id_id=request.user.id)
        messages.success(request, "Request sent successfully")
        
        return redirect("/houses/" + str(house_id))

    return HttpResponse('404')


def acceptRequest(request, house_id, user_id):

    rentRequest = Requests.objects.raw('SELECT * FROM rent_app_requests where house_id_id = ' + str(house_id) + ' and user_id_id = ' + str(user_id))

    if len(rentRequest) == 0:
        return HttpResponse('<h1>Page not found</h1>')

    reqHouse = House.objects.raw('SELECT * FROM rent_app_house where house_id = ' + str(house_id))[0]
    if reqHouse.owner_id.pk != request.user.id:
        return HttpResponse('You are not authorized to do this action!')

    user = CustomUser.objects.raw('SELECT * FROM rent_app_customuser where id = ' + str(user_id))[0]

    # Main logic of accepting the user
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM rent_app_requests WHERE house_id_id = %s', [house_id])
        cursor.execute('UPDATE rent_app_house SET vacant = 0, rented_id = %s where house_id = %s', (user_id, house_id))
    
    
    subject = 'Rent request accepted!'
    message = f'Hi {user.user_name}, The house http://127.0.0.1:8000/houses/{house_id} you wanted to rent is now accepted by the owner. Visit the house view page whenever you want to leave or you can contact the owner anytime\n\nThank you'
    emailSender(subject, message, user.email)
    
    return redirect('/houses/' + str(house_id))


def leaveHouse(request, house_id):
    house = House.objects.raw("SELECT * FROM rent_app_house where house_id = " + str(house_id))[0]
    
    if house.vacant == 1:
        return HttpResponse("The requested page doesn't exist")

    if house.owner_id.pk == request.user.id:
        return HttpResponse('Contact the admin if you want to remove the user from your house')

    if house.rented_id != request.user.id:
        return HttpResponse("The requested page doesn't exist")

    with connection.cursor() as cursor:
        cursor.execute('UPDATE rent_app_house SET vacant = 1, rented_id = -1 where house_id = %s', [house_id])
    return redirect('/houses/' + str(house_id))


def editHouse(request, house_id):
    return HttpResponse('edit house')