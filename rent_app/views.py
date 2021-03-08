# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .models import user_type, User


def HomePage(request):
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


# def signup(request):
#     if (request.method == 'POST'):
#         # print(request.POST)
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         owner1 = request.POST.get('owner')
#         user1 = request.POST.get('user')
        
#         user = User.objects.create_user(
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
        
#         usert = None
#         if owner1:
#             usert = user_type(user=user, is_owner=True)
#         elif user1:
#             usert = user_type(user=user, is_user=True)
        
#         usert.save()
#         #Successfully registered. Redirect to homepage
#         # return redirect('home')
#         print('sign1111')
#     return render(request, 'register.html')


# def login(request):
#     if (request.method == 'POST'):
#         email = request.POST.get('email') #Get email value from form
#         password = request.POST.get('password') #Get password value from form
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             type_obj = user_type.objects.get(user=user)
#             if user.is_authenticated and type_obj.is_student:
#                 # return redirect('shome') #Go to student home
#                 print('world1')
#             elif user.is_authenticated and type_obj.is_teach:
#                 print('hello1')
#                 # return redirect('') #Go to teacher home
#         else:
#             # Invalid email or password. Handle as you wish
#             print('here1')
#             return redirect('home')

#     return render(request, 'login.html')