from rest_framework import serializers
from rest_framework.serializers import Serializer, ImageField, EmailField
from .models import User,Advisor
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class UserSerializer(serializers.HyperlinkedModelSerializer):

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

class AdvisorSerializer(serializers.HyperlinkedModelSerializer):
    photo = ImageField()
    class Meta:
        model = Advisor
        fields = ['name', 'photo']
