from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator


class User(models.Model):

    # null  = True -> This attribute in the database can be NULL
    # blank = True -> This attribute is not required in the form, if it is false the field can't be blank in the form

    user_id         = models.AutoField(primary_key=True)
    username        = models.CharField(max_length=100, unique=True)
    user_email      = models.EmailField(max_length = 100, unique=True) 
    password        = models.CharField(max_length=100)
    phone           = models.IntegerField(unique=True, validators=[MaxLengthValidator(10),MinLengthValidator(10)])
    image           = models.ImageField(upload_to='images/', null=True) 
    adress          = models.TextField(null=True)
    upi_id          = models.CharField(max_length = 100, null=True, unique=True) 
    document        = models.ImageField(upload_to='images/', null=True) 

    def __str__(self):
        return self.username


class Owner(models.Model):
    owner_id        = models.AutoField(primary_key=True)
    username        = models.CharField(max_length=100, unique=True)
    owner_email     = models.EmailField(max_length = 100, unique=True) 
    password        = models.CharField(max_length=100)
    phone           = models.IntegerField(unique=True, validators=[MaxLengthValidator(10),MinLengthValidator(10)])
    image           = models.ImageField(upload_to='images/',null=True) 
    adress          = models.TextField(null=True)
    upi_id          = models.CharField(max_length = 100, null=True, unique=True) 

    def __str__(self):
        return self.username


class House(models.Model):
    house_id        = models.AutoField(primary_key=True)
    city            = models.CharField(max_length=100, )
    state           = models.CharField(max_length=100)
    address         = models.TextField()
    rent            = models.IntegerField()
    owner_id        = models.ForeignKey(Owner,on_delete=models.CASCADE)
    description     = models.TextField(null=True)
    vacant          = models.BooleanField

    def __str__(self):
        return self.address


class HouseImages(models.Model):
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='images/', null=False)
    id              = models.AutoField(primary_key=True)


# class Review(models.Model):