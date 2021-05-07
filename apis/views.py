from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User, Advisor, Booking
from apis.serializers import AdvisorSerializer, RegisterUserSerializer, LoginUserSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows users to register.
    """

    serializer_class = RegisterUserSerializer
    def post(self,request):
        request_data = request.data
        #request_data.is_active = True
        user_serializer = RegisterUserSerializer(data=request_data)
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
    API endpoint that allows users to login.
    """

    serializer_class = LoginUserSerializer
    queryset = User.objects.all()
    def post(self,request):
        user_serializer = LoginUserSerializer(data=request.data)
        if user_serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user = user_serializer.authenticate_user(email,password)
            if user is not None:
                user.username = user.email
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
            
class ListAdvisorView(generics.CreateAPIView):
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

class AddBookingView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    """
    API endpoint that lists advisors.
    """

    def post(self,request, *args, **kwargs):
        user_id=self.kwargs.get('user_id')
        advisor_id=self.kwargs.get('advisor_id')
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
            if booking_serializer.check_booking_time_available(advisor_id,booking_time):
                if booking_serializer.is_valid():
                    booking_serializer = booking_serializer.save()
                    return Response([], status=status.HTTP_200_OK)
                else:
                    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBookingView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    """
    API endpoint that lists advisors.
    """

    def get(self,request, *args, **kwargs):
        user_id=self.kwargs.get('user_id')
        res = []
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            bookings = user.bookings.all()
            serializer = BookingSerializer(bookings,many = True)
            booking_array = serializer.data
            
            for booking in bookings:
                #advisor = Advisor.objects.get(id=booking.advisor)
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

            

       