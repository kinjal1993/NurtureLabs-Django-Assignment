from rest_framework import serializers
from rest_framework.serializers import Serializer, ImageField
from .models import User,Advisor

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']

class AdvisorSerializer(serializers.HyperlinkedModelSerializer):
    photo = ImageField()
    class Meta:
        model = Advisor
        fields = ['name', 'photo']
