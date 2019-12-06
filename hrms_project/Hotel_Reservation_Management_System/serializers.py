from rest_framework import serializers
from Hotel_Reservation_Management_System.models import *

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'room_type', 'room_price_per_night',)

class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id','name', 'address', 'contact_number')

class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'room', 'guest', 'number_of_guest', 'check_in_date', 'checked_in', 'number_of_nights_of_stay', 'checked_out', "cancel_booking",)

# class RoomSerializers(serializers.Serializer):
    # id = serializers.I