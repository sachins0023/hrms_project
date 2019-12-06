from django.contrib import admin
from Hotel_Reservation_Management_System.models import *
from django import forms
import re

# Register your models here.

class RoomAdminForm(forms.ModelForm):
    """
    Does field validation for room_type and disables occupied field completely and room_number if trying to edit the
    room. Also checks if a room is already occupied. Checking if the room already exists in the database.
    """
    def __init__(self, *args, **kwargs):
        super(RoomAdminForm, self).__init__(*args, **kwargs)

        if not self.instance.id:
            self.fields['occupied'].disabled = True
        else:
            self.fields['occupied'].disabled = True
            self.fields['room_number'].disabled = True

    def clean(self):
        types_of_rooms = ['Deluxe', 'Super Deluxe', 'Premium']
        room_type = self.cleaned_data.get('room_type')
        room_number = self.cleaned_data.get('room_number')
        if room_number is not None:
            if any(Room.objects.exclude(id = self.instance.id).filter(room_number = room_number)):
                raise forms.ValidationError("The particular room number exits is in database. Please choose a different room number")
        if room_type is not None:
            if room_type not in types_of_rooms:
                raise forms.ValidationError("Room type should be one of Deluxe, Super Deluxe, or Premium. Please enter a valid room type.",
                                            code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(RoomAdminForm, self).save(commit = commit)


class RoomAdmin(admin.ModelAdmin):
    """
    Displays the list of rooms in the database
    """
    list_display = ('room_number','room_type', 'occupied', 'room_price_per_night',)
    ordering = ('room_number',)
    list_filter = ('occupied','room_type')
    search_fields = ['room_type',]
    form = RoomAdminForm

admin.site.register(Room, RoomAdmin)


class GuestAdminForm(forms.ModelForm):
    """
    Does validation for contact_number and number_of_guests
    """
    def __init__(self, *args, **kwargs):
        super(GuestAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
         Checking contact number validity, Checking if the guest record exists in the database
        """
        contact_number = self.cleaned_data.get('contact_number')
        name = self.cleaned_data.get('name')
        if contact_number is not None:
            regex = r"^\d{10}$"
            match = re.search(regex, contact_number)
            if match is None:
                raise forms.ValidationError("The entered contact number is invalid. Please enter a 10 digit value.", code = 'invalid')
            if name is not None:
                if any(Guest.objects.exclude(id = self.instance.id).filter(name = name, contact_number = contact_number)):
                    raise forms.ValidationError("The guest is already present in the database.")
        return self.cleaned_data

    def save(self, commit = True):
        return super(GuestAdminForm, self).save(commit = commit)


class GuestAdmin(admin.ModelAdmin):
    """
    Displays the list of Guests
    """
    list_display = ('name', 'address', 'contact_number',)
    ordering = ('name',)
    search_fields = ['name',]
    form = GuestAdminForm

admin.site.register(Guest,GuestAdmin)

class BookingAdminForm(forms.ModelForm):
    """
    Does validation for room whether it is occupied or not and checking if number of guests is less than 4,
    number of nights of stay should be a positive integer too, Guest should not be able to book more than one room if
    he is checked in or has a booking
    """
    def __init__(self, *args, **kwargs):
        super(BookingAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.id:
            self.fields['checked_out'].disabled = True
            self.fields['cancel_booking'].disabled = True
        else:
            if self.instance.checked_in == True:
                self.fields['room'].disabled = True
                self.fields['guest'].disabled = True
                self.fields['check_in_date'].disabled = True
                self.fields['checked_in'].disabled = True
                self.fields['cancel_booking'].disabled = True
            else:
                self.fields['checked_out'].disabled = True
            if self.instance.checked_out == True or self.instance.cancel_booking == True:
                l = ['room', 'guest', 'check_in_date', 'checked_in', 'checked_out', 'cancel_booking', 'number_of_guest', 'number_of_nights_of_stay']
                for i in l:
                    self.fields[i].disabled = True

    def clean(self):
        number_of_nights_of_stay = self.cleaned_data.get('number_of_nights_of_stay')
        room = self.cleaned_data.get('room')
        number_of_guest = self.cleaned_data.get('number_of_guest')
        guest = self.cleaned_data.get('guest')

        if room is not None:
            if room.occupied == True and self.cleaned_data.get('checked_out') == False:
                if (self.cleaned_data.get('check_in_date') <= Booking.objects.exclude(id = self.instance.id).filter(room = room, checked_out=False)[0].check_out_date()): #or \
                        # ((self.cleaned_data.get('check_in_date') <= Booking.objects.exclude(id = self.instance.id).filter(room = room, checked_out = False)[0].check_in_date) and \
                        #  (self.cleaned_data.get('check_out_date') >= Booking.objects.exclude(id = self.instance.id).filter(room = room, checked_out = False)[0].check_out_date())):
                    raise forms.ValidationError("Room already occupied. Please assign a different room for the guest.")
            """elif room.occupied == False and self.cleaned_data.get('checked_out') == False:
                # if self.cleaned_data.get('check_out_date') is not None:
                if self.cleaned_data.get('check_in_date') <= Booking.objects.exclude(id = self.instance.id).filter(room = room, checked_out = False).get(guest = guest).check_in_date:
                    if self.cleaned_data.get('check_in_date')+timedelta(days = number_of_nights_of_stay) >= Booking.objects.exclude(id = self.instance.id).filter(room = room, checked_out = False).get(guest = guest).check_in_date:
                        raise forms.ValidationError("Room occupied during some of the dates of duration of stay. Please select a different room")"""

        if guest is not None:
            if any(Booking.objects.exclude(id = self.instance.id).filter(guest = guest, checked_out = False)):
                if self.cleaned_data.get('check_in_date') <= Booking.objects.exclude(id = self.instance.id).filter(guest = guest,
                                                                                                                 checked_out = False)[0].check_out_date():
                    raise forms.ValidationError("Guest already booked a room. Please make changes to your current booking")
        if number_of_nights_of_stay is not None:
            if number_of_nights_of_stay<1:
                raise forms.ValidationError("Invalid input for Number of nights of stay. Should be 1 or more.")
        if number_of_guest is not None:
            if number_of_guest>3 or number_of_guest<1:
                raise forms.ValidationError("Invalid Number of guests. Number of guests must be between 1 and 3.")
        return self.cleaned_data

    def save(self, commit=True):
        return super(BookingAdminForm, self).save(commit=commit)

class BookingAdmin(admin.ModelAdmin):
    """
    Displays the records of bookings
    """
    list_display = ('room_number', 'guest_name', 'room_type', 'number_of_guest', 'contact_number',
                    'check_in_date', 'checked_in', 'check_out_date', 'checked_out', 'number_of_nights_of_stay',
                    'room_price_per_night', 'cost_of_stay', 'cancel_booking')
    list_filter = ('room__room_type', 'checked_in', 'checked_out', 'cancel_booking')
    search_fields = ['guest_name',]
    form = BookingAdminForm

admin.site.register(Booking, BookingAdmin)