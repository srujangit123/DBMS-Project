from django.contrib import admin
from .models import User, Owner, House, HouseImages, Review, House_Management


admin.site.register(User)
admin.site.register(Owner)
admin.site.register(House)
admin.site.register(HouseImages)
admin.site.register(Review)
admin.site.register(House_Management)