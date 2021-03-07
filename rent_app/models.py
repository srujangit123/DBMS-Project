from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator


RATING_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)


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
    vacant          = models.BooleanField(default=False)

    def __str__(self):
        return self.address


class HouseImages(models.Model):
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='images/', null=False)
    id              = models.AutoField(primary_key=True)


class Review(models.Model):
    # Review id will be auto generated.
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    description     = models.CharField(max_length=100)
    rating          = models.CharField(max_length=20, choices=RATING_CHOICES, null=False)
    # A single user can give review only once => The tuple (user_id, house_id) is unique in Review table
    class Meta:
        unique_together = (
            ('user_id', 'house_id'),
        )


class House_Management(models.Model):
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    house_id        = models.ForeignKey(House, on_delete=models.CASCADE)
    owner_id        = models.ForeignKey(Owner,on_delete=models.CASCADE)
    date_time       = models.DateTimeField(auto_now_add=True)
