from django.shortcuts import render
from Hotel_Reservation_Management_System.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from Hotel_Reservation_Management_System.serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.

@api_view(['GET',])
def api_room_list_view(request):
    room = Room.objects.all()
    if request.method == 'GET':
        serializer = RoomSerializers(room, many = True)
        return Response(serializer.data)

@api_view(['PUT',])
def api_update_room_list_view(request, id):
    try:
        room = Room.objects.get(id = id)
    except Room.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = RoomSerializers(room, data = request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data['Success'] = 'Update successful'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST', ])
def api_create_room_details_view(request):
    print(request.method)
    if request.method == 'POST':
        serializer = RoomSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {}
            data['Success'] = 'Created Successfully'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    return Response(status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE',])
def api_delete_room_details_view(request, id):
    try:
        room = Room.objects.get(id = id)
    except Room.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        room.delete()
        data['Delete'] = 'Delete operation Successful'
        return Response(data, status.HTTP_200_OK)

@api_view(['GET',])
def api_booking_list_view(request):
    booking = Booking.objects.all()
    if request.method == 'GET':
        serializer = BookingSerializers(booking, many = True)
        return Response(serializer.data)

@api_view(['GET',])
def api_guest_list_view(request):
    guest = Guest.objects.all()
    if request.method == 'GET':
        serializer = GuestSerializers(guest, many = True)
        return Response(serializer.data)

@api_view(['GET',])
def api_guest_id_details(request, id):
    try:
        guest = Guest.objects.get(id = id)
    except Guest.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializers(guest)
        return Response(serializer.data)

@api_view(['PUT',])
def api_update_guest_list_view(request, id):
    try:
        guest = Guest.objects.get(id = id)
    except Guest.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = GuestSerializers(guest, data = request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data['Success'] = 'Update successful'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST',])
def api_create_guest_details_view(request):
    if request.method == 'POST':
        guest = Guest.objects.create(data = request.data)
        serializer = GuestSerializers(guest, data = request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data['Success'] = 'Created Successfully'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE',])
def api_delete_guest_details_view(request, id):
    try:
        guest = Guest.objects.get(id = id)
    except Guest.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        guest.delete()
        data['Delete'] = 'Delete operation Successful'
        return Response(data, status.HTTP_200_OK)

@api_view(['PUT',])
def api_update_booking_list_view(request, id):
    try:
        booking = Booking.objects.get(id = id)
    except Booking.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = BookingSerializers(booking, data = request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data['Success'] = 'Update successful'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST',])
def api_create_booking_details_view(request):
    if request.method == 'POST':
        booking = Booking.objects.create(data = request.data)
        serializer = BookingSerializers(booking, data = request.data)
        if serializer.is_valid():
            data = {}
            serializer.save()
            data['Success'] = 'Created Successfully'
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE',])
def api_delete_booking_details_view(request, id):
    try:
        booking = Booking.objects.get(id = id)
    except Booking.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        booking.delete()
        data['Delete'] = 'Delete operation Successful'
        return Response(data, status.HTTP_200_OK)


@api_view(['GET',])
def api_room_id_details(request, id):
    try:
        room = Room.objects.get(id = id)
    except Room.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializers(room)
        return Response(serializer.data)


@api_view(['GET',])
def api_booking_id_details(request, id):
    try:
        booking = Booking.objects.get(id = id)
    except Booking.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializers(booking)
        return Response(serializer.data)







# class RoomView(viewsets.ModelViewSet):
#     serializer_class = RoomSerializers
#     queryset = Room.objects.all()
#
# class GuestView(viewsets.ModelViewSet):
#     serializer_class = GuestSerializers
#     queryset = Guest.objects.all()
#
# class BookingView(viewsets.ModelViewSet):
#     serializer_class = BookingSerializers
#     queryset = Booking.objects.all()


