from django.contrib import admin
from .models import House, HouseImages, User, Owner


admin.site.register(User)
admin.site.register(House)
admin.site.register(HouseImages)
admin.site.register(Owner)