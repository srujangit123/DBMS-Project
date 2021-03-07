"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import path
from rent_app.views import HomePage, Login, Register
>>>>>>> 17c217a0713a70074804b343f96f27894b69fc30

urlpatterns = [
    path('',include('rent_app.urls')),
    path('admin/', admin.site.urls),
    path('', HomePage),
    path('login/', Login),
    path('register/', Register)
]
