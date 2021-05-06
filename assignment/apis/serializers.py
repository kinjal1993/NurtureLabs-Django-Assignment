from rest_framework import serializers
from rest_framework.serializers import Serializer, ImageField, EmailField, DateTimeField
from .models import User,Advisor,Booking
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):

    email = serializers.EmailField()
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already exists")
        return lower_email

    def validate_password(self, value):
        password = value
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(' '.join([str(elem) for elem in e]))

        return value


    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

class LoginUserSerializer(serializers.HyperlinkedModelSerializer):

    def authenticate_user(self,email,password):
        try:
            user = User.objects.get(email=email,password=password)
            return user
        except User.DoesNotExist:
            return None
        
        return None

    class Meta:
        model = User
        fields = ['email', 'password']

class AdvisorSerializer(serializers.HyperlinkedModelSerializer):
    photo = ImageField()
    class Meta:
        model = Advisor
        fields = ['id','name', 'photo']

class BookingSerializer(serializers.ModelSerializer):
    booking_time = DateTimeField()
    advisor = serializers.PrimaryKeyRelatedField(queryset=Advisor.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Booking
        fields = ['id','booking_time', 'advisor', 'user']

