from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username        = None
    email           = models.EmailField(_('email address'), unique=True)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phoneno         = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True) # validators should be a list
    upi_id          = models.CharField(max_length=255, null=True)
    address         = models.CharField(max_length=255, null=True)
    user_name       = models.CharField(max_length=20, null=True)
    profile_image   = models.ImageField(upload_to='profile_images/', null=True)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects         = CustomUserManager()

    def __str__(self):
        return self.email