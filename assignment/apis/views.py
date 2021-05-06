from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User, Advisor
from apis.serializers import AddAdvisorSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows users to register.
    """

    serializer_class = RegisterUserSerializer
    def post(self,request):
        user_serializer = RegisterUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            refresh = RefreshToken.for_user(user)
            res = {
                "token": str(refresh.access_token),
                "id" : user.id
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    """
    API endpoint that allows users to register.
    """

    serializer_class = LoginUserSerializer
    queryset = User.objects.all()
    def post(self,request):
        user_serializer = LoginUserSerializer(data=request.data)
        if user_serializer.is_valid():
            #user = user_serializer.save()
            
            email = request.data.get('email')
            password = request.data.get('password')
            user = user_serializer.authenticate_user(email,password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                res = {
                    "token": str(refresh.access_token),
                    "id" : user.id
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAdvisorView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddAdvisorSerializer
    queryset = Advisor.objects.all()
    """
    API endpoint that allows to add advisors.
    """

    def post(self,request):
        file_serializer = AddAdvisorSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response([], status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       