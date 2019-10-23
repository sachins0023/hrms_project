from rest_framework import viewsets
from rest_framework import routers
from Hotel_Reservation_Management_System import views
from django.urls import path, include
from Hotel_Reservation_Management_System.views import *
from django.urls import path
# router = routers.DefaultRouter()
# router.register('room', views.RoomView)
# router.register('guest', views.GuestView)
# router.register('booking', views.BookingView)

app_name = 'Hotel_Reservation_Management_System'

urlpatterns = [
    # path('', include(router.urls))
    path('room/', api_room_list_view, name = 'room'),
    path('booking/', api_booking_list_view, name = 'booking'),
    path('booking/<int:id>/', api_booking_id_details, name = 'booking_id'),
    path('guest/', api_guest_list_view, name = 'guest'),
    path('guest/<int:id>/', api_guest_id_details, name = 'guest_id'),
    path('room/<int:id>/', api_room_id_details, name = 'room_id'),
    path('room/<int:id>/update/', api_update_room_list_view, name = 'room_update'),
    path('guest/<int:id>/update/', api_update_guest_list_view, name = 'guest_update'),
    path('booking/<int:id>/update/', api_update_booking_list_view, name = 'booking_update'),
    path('room/create/', api_create_room_details_view, name = 'room_creation'),
    path('guest/create/', api_create_guest_details_view, name = 'guest_creation'),
    path('booking/create/', api_create_booking_details_view, name = 'booking_creation'),
    path('room/<int:id>/delete/', api_delete_room_details_view, name = 'room_deletion'),
    path('guest/<int:id>/delete/', api_delete_guest_details_view, name = 'guest_deletion'),
    path('booking/<int:id>/delete/', api_delete_booking_details_view, name = 'booking_deletion'),
]