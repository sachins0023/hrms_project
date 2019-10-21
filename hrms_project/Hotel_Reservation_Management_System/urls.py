from rest_framework import viewsets
from rest_framework import routers
from Hotel_Reservation_Management_System import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('room', views.RoomView)
router.register('guest', views.GuestView)
router.register('booking', views.BookingView)

urlpatterns = [
    path('', include(router.urls))
]