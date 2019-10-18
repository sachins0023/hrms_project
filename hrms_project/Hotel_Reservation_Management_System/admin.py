from django.contrib import admin
from Hotel_Reservation_Management_System.models import *
from django import forms
import re


# Register your models here.

class RoomAdminForm(forms.ModelForm):
    """
    Does field validation for room_type and disables occupied field completely and room_number if trying to edit the
    room. Also checks if a room is already occupied.
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
         Checking contact number validity
        """
        contact_number = self.cleaned_data.get('contact_number')
        number_of_guest = self.cleaned_data.get('number_of_guest')
        if contact_number is not None:

            regex = r"^\d{10}$"
            match = re.search(regex, contact_number)
            if match is None:
                raise forms.ValidationError("The entered contact number is invalid. Please enter a 10 digit value.", code = 'ivalid')

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
    number of nights of stay should be a positive integer too
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

    def clean(self):
        number_of_nights_of_stay = self.cleaned_data.get('number_of_nights_of_stay')
        room_ = self.cleaned_data.get('room')
        number_of_guest = self.cleaned_data.get('number_of_guest')
        guest = self.cleaned_data.get('guest')
        if guest is not None:
            if any(Booking.objects.filter(room = room_, guest = guest, checked_out = False)): #### Error is here
                raise forms.ValidationError("Guest already booked a room. Please checkout to book a new room")
        if room_ is not None:
            if room_.occupied == True:
                raise forms.ValidationError("Room already occupied. Please assign a different room for the guest.")
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
                    'check_in_date', 'checked_in', 'check_out_date', 'checked_out', 'room_price_per_night',
                    'cost_of_stay', 'cancel_booking')
    list_filter = ('room__room_type',)
    search_fields = ['guest_name',]
    form = BookingAdminForm

admin.site.register(Booking, BookingAdmin)