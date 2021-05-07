from rest_framework import serializers
from rest_framework.serializers import Serializer, ImageField, EmailField, DateTimeField
from .models import User,Advisor,Booking
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from datetime import datetime

class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):

    email = serializers.EmailField()
    USERNAME_FIELD = 'email'

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

    USERNAME_FIELD = 'email'

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

    def validate_booking_time(self,value): # check if booking time is greater than today
        input = value
        present = datetime.now()
        minutes = int(input.strftime("%M"))
        if input.date() < present.date():
            raise serializers.ValidationError("Booking time should be greater than today!")
        elif minutes % 15 != 0:
            raise serializers.ValidationError("Booking time should be at every quarter of every hour!")
        else:
            return value 
            

    def check_booking_time_available(self,advisor_id,booking_time):
        advisor = Advisor.objects.get(id=advisor_id)
        booking = advisor.booked_advisors.filter(booking_time=booking_time)
        
        if not booking:
            return True
        else:
            raise serializers.ValidationError("Booking time is already booked!")
