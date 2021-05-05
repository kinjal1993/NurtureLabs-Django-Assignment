from django.db import models

# Create your models here.

class Advisor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='router_specifications')

    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name