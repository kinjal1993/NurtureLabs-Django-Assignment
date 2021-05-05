from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User, Advisor
from apis.serializers import UserSerializer, AdvisorSerializer

class UserList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many = True)
        return Response(serializer.data)


class AdvisorList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self,request):
        advisors = Advisor.objects.all()
        serializer = AdvisorSerializer(advisors,many = True)
        return Response(serializer.data)

    def post(self,request):
        file_serializer = AdvisorSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       