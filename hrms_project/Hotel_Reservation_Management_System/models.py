from django.db import models
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# Create your models here.

class Room(models.Model):
    room_number = models.IntegerField(default = 101)
    occupied = models.BooleanField(default = False)
    room_type = models.CharField(default = 'Deluxe', max_length = 20)

    def __str__(self):
        return str(self.room_number)

    def room_price_per_night(self):
        if self.room_type == 'Deluxe':
            return 1500.0
        elif self.room_type == 'Super Deluxe':
            return 2500.0
        elif self.room_type == 'Premium':
            return 4000.0

class Guest(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    contact_number = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete = models.CASCADE)
    number_of_guest = models.IntegerField(default=1)
    check_in_date = models.DateField(default = datetime.now())
    checked_in = models.BooleanField(default = False)
    number_of_nights_of_stay = models.IntegerField(default = 1)
    checked_out = models.BooleanField(default = False)
    cancel_booking = models.BooleanField(default = False)

    def check_out_date(self):
        return self.check_in_date + timedelta(days = self.number_of_nights_of_stay)

    # @property
    def room_number(self):
        return self.room.room_number

    # @property
    def room_type(self):
        return self.room.room_type

    # @property
    def room_price_per_night(self):
        return self.room.room_price_per_night()

    # @property
    def guest_name(self):
        return self.guest.name

    # @property
    def contact_number(self):
        return self.guest.contact_number

    # @property
    def cost_of_stay(self):
        return self.number_of_nights_of_stay * self.room_price_per_night()

    def __str__(self):
        return 'booking '+str(self.id)

@receiver(post_save, sender = Booking)
def add_occupant(sender, instance, created, **kwargs):
    """
    occupied in Room has to become True
    """
    room = instance.room
    if created:
        if instance.checked_in == True:
            room.occupied = True
        room.save()
    if instance.checked_out == True:
        room.occupied = False
        room.save()