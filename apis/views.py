from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User, Advisor, Booking
from apis.serializers import AdvisorSerializer, UserSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse

# welcome page
def init_view(request):
    return HttpResponse("NurtureLabs Intern API Assignment")

class UserView(generics.CreateAPIView):
    """
    API endpoint that allows users to register & login.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self,request): # login api
        email = request.data.get('email')
        password = request.data.get('password')

        if email is not None and password is not None: # check if email password set in request
            try:
                user = User.objects.get(email=email,password=password) # check if credentials are valid
                if user is not None:
                    refresh = RefreshToken.for_user(user) # if user is valid generate token
                    res = {
                        "token": str(refresh.access_token),
                        "id" : user.id
                    }
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_401_UNAUTHORIZED) # if credentials are wrong
            except User.DoesNotExist:
                return Response([], status=status.HTTP_401_UNAUTHORIZED) # if credentials are wrong
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST) # if email password not set
    
    def post(self,request): # register api
        request_data = request.data
        user_serializer = UserSerializer(data=request_data)
        if user_serializer.is_valid(): # check if request params are valid
            user = user_serializer.save() # generate user
            refresh = RefreshToken.for_user(user) # generate token after user generated
            res = {
                "token": str(refresh.access_token),
                "id" : user.id
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) # check if request params are invalid


class AddAdvisorView(generics.CreateAPIView): # add advisor api
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvisorSerializer
    queryset = Advisor.objects.all()
    """
    API endpoint that allows to add advisors.
    """

    def post(self,request):
        file_serializer = AdvisorSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response([], status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ListAdvisorView(generics.CreateAPIView): # list advisor api
    permission_classes = (IsAuthenticated, )
    serializer_class = AdvisorSerializer
    queryset = Advisor.objects.all()
    """
    API endpoint that lists advisors.
    """

    def get(self,request, *args, **kwargs):
        user_id=self.kwargs.get('user_id')
        advisors = Advisor.objects.all()
        serializer = AdvisorSerializer(advisors,many = True)
        return Response(serializer.data)

class BookingView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    """
    API endpoint that lists and adds bookings.
    """

    def get(self,request, *args, **kwargs):  # list bookings api
        user_id=self.kwargs.get('user_id')
        res = []
        # check if user exists with user id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            bookings = user.bookings.all() # fetch all bookings for the user
            
            for booking in bookings:
                # fetch advisor object for each booking
                advisor = AdvisorSerializer(booking.advisor)
                # format date into dd/mm/yyyy
                booking_time = booking.booking_time.strftime("%d/%m/%Y %H:%M:%S")
                temp = {
                    'id' : booking.id,
                    'booking_time' : booking_time,
                    'advisor' : advisor.data
                }
                res.append(temp)
        
        return Response(res)

    def post(self,request, *args, **kwargs): # make booking api
        user_id=self.kwargs.get('user_id')
        advisor_id=self.kwargs.get('advisor_id')

        # check if user & advisor exists with respective id
        advisor = Advisor.objects.get(id=advisor_id)
        user = User.objects.get(id=user_id)
        
        if user is not None and advisor is not None:
            booking_time = request.data.get('booking_time')
            data = {
                'user':user_id, 
                'advisor':advisor_id, 
                'booking_time':booking_time, 
            }
            
            booking_serializer = BookingSerializer(data=data)
            # check if booking time is avalable & valid then book the appointment
            if booking_serializer.check_booking_time_available(advisor_id,booking_time):
                if booking_serializer.is_valid():
                    booking_serializer = booking_serializer.save()
                    return Response([], status=status.HTTP_200_OK)
                else:
                    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            

       