from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from users.models import CustomUser, CustomUserManager


RATING_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)

class House(models.Model):
    house_id        = models.AutoField(primary_key=True)
    city            = models.CharField(max_length=100, )
    state           = models.CharField(max_length=100)
    address         = models.TextField()
    rent            = models.IntegerField()
    owner_id        = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description     = models.TextField(null=True)
    vacant          = models.BooleanField(default=True)
    rented_id       = models.IntegerField(default=-1)

    def __str__(self):
        return self.address

# select image from HouseImages inner join House where HouseImages.house_id=House.house_id
class HouseImages(models.Model):
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='house_images/', null=False)
    id              = models.AutoField(primary_key=True)


class Review(models.Model):
    # Review id will be auto generated.
    user_id         = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    description     = models.CharField(max_length=100)
    rating          = models.CharField(max_length=20, choices=RATING_CHOICES, null=False)
    # A single user can give review only once => The tuple (user_id, house_id) is unique in Review table
    class Meta:
        unique_together = (
            ('user_id', 'house_id'),
        )


class Requests(models.Model):
    user_id         = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)