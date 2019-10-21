from django.shortcuts import render
from Hotel_Reservation_Management_System.models import *
from rest_framework import viewsets
from Hotel_Reservation_Management_System.serializers import *

# Create your views here.

class RoomView(viewsets.ModelViewSet):
    serializer_class = RoomSerializers
    queryset = Room.objects.all()

class GuestView(viewsets.ModelViewSet):
    serializer_class = GuestSerializers
    queryset = Guest.objects.all()

class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializers
    queryset = Booking.objects.all()


