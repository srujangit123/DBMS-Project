from django.contrib import admin
from django.urls import path, re_path, include
from rent_app.views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    re_path('^$', HomePage),
    path('about/', about),
    path('services/', services),
    path('contact/', contact),
    path('houses/add', addHouse, name='addhouse'),
    path('houses/<int:house_id>', viewHouse, name='view_house'),
    path('houses/add_house', addHouse, name='add_house'),
    path('request/<int:house_id>', sendRentRequest, name='send_request'),
    path('houses/edit/<int:house_id>', editHouse, name='edit_house'),
    path('leave/<int:house_id>', leaveHouse, name='leave_house'),
    path('requests/accept/<int:house_id>/<int:user_id>',acceptRequest, name='accept_request'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 