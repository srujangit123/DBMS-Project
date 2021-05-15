from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.signup, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('edit/', views.update_profile, name='update_profile'),
]

