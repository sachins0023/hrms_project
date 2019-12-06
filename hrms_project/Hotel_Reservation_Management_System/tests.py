from django.test import TestCase
from Hotel_Reservation_Management_System.models import *
from datetime import date

# Create your tests here.

class RoomTestCase(TestCase):
    """
    Test case 1: testing room price per night function in Room
    """
    def setUp(self):
        Room.objects.create(room_number = 101, room_type = 'Premium')

    def test_case_find_room_price(self):
        room = Room.objects.get(room_number = 101)
        self.assertEqual(room.room_price_per_night(), 4000.0)


class BookingTestCase(TestCase):
    """
    Testcase 2-8: testing check out date, room number, room type, room price per night, guest name, contact number,
    cost of stay
    """
    def setUp(self):
        room = Room.objects.create(room_number = 110, room_type = 'Premium')
        guest = Guest.objects.create(name = 'Sachin', address = 'Bengaluru', contact_number = '1234567890')
        Booking.objects.create(room = room, guest = guest, number_of_guest = 3, check_in_date = '2019-10-19', checked_in = True, number_of_nights_of_stay = 4)

    def test_case_check_out_date(self):
        """
        Testcase 2: Checks whether the checkout date outputted is correct
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest = guest)
        self.assertEqual(booking.check_out_date(), date(2019,10,23))

    def test_case_booking_room_number(self):
        """
        Testcase 3: Checks whether the room number from the Room model is captured properly by Booking
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest = guest)
        self.assertEqual(booking.room_number(), 110)

    def test_case_booking_room_type(self):
        """
        Testcase 4 : Checks whether the room type from the Room model is captured properly by Booking
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest=guest)
        self.assertEqual(booking.room_type(), 'Premium')

    def test_case_booking_room_price_per_night(self):
        """
        Testcase 5: Checks whether the room price from the Room model is captured properly by Booking
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest=guest)
        self.assertEqual(booking.room_price_per_night(), 4000.0)

    def test_case_guest_name(self):
        """
        Testcase 6: Checks whether the guest name from the Guest model is captured properly by Booking
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest=guest)
        self.assertEqual(booking.guest_name(), 'Sachin')

    def test_case_contact_number(self):
        """
        Testcase 7: Checks whether the contact number from the Guest model is captured properly by Booking
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest=guest)
        self.assertEqual(booking.contact_number(), '1234567890')

    def test_case_cost_of_stay(self):
        """
        Testcase 8 : Checks whether the calculated total cost of stay is correct
        """
        guest = Guest.objects.get(name='Sachin', address='Bengaluru', contact_number='1234567890')
        booking = Booking.objects.get(guest=guest)
        self.assertEqual(booking.cost_of_stay(), 16000.0)
