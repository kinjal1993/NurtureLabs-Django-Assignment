from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.

class Advisor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='router_specifications')

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'name' ]

    # def __str__(self):
    #     return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='booked_advisors')
    booking_time = models.DateTimeField()
