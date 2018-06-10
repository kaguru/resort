from django.test import TestCase
from django.urls import reverse
import tempfile
from django.contrib.auth.models import User
from booking import models as booking_models
from datetime import datetime, date

class UserProfileTest(TestCase):

    @classmethod
    def setUp(cls):
        user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gdot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }
        user = User.objects.create_user(**user_data)
        profile_pic = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.userprofile_data = {
            'user': user,
            'profile_pic': profile_pic,
        }

    def create_userprofile(self, **kwargs):
        userprofile_obj = booking_models.UserProfile.objects.create(**kwargs)
        return userprofile_obj

    def test_create_userprofile_model(self):
        '''Valid data gets submitted through UserProfile Model'''
        userprofile_obj = self.create_userprofile(**self.userprofile_data)
        self.assertTrue(isinstance(userprofile_obj, booking_models.UserProfile))

    def test_null_user_userprofile_model(self):
        '''InValid data (null user field) doesn\'t gets submitted through UserProfile Model'''
        try:
            userprofile_obj = self.create_userprofile(user=None)
        except:
            pass
        self.assertRaises(Exception)

    def test_absolute_url(self):
        '''Check UserProfile Model Absolute Url  '''
        userprofile_obj = self.create_userprofile(**self.userprofile_data)
        self.assertEqual(userprofile_obj.get_absolute_url(), reverse('booking:profile-detail', kwargs={'pk': userprofile_obj.user.pk} ))

    def test_str_url(self):
        '''Check Str for USer Profile '''
        userprofile_obj = self.create_userprofile(**self.userprofile_data)
        self.assertEqual(userprofile_obj.__str__(), userprofile_obj.user.username)

class RoomStandardTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.room_std_name = 'Executive'

    def create_room_standard(self, **kwargs):
        room_std_obj = booking_models.RoomStandard.objects.create(**kwargs)
        return room_std_obj

    def test_room_standard_create(self):
        '''Create RoomStandard (Model)'''
        room_std_obj = self.create_room_standard(name=self.room_std_name)
        self.assertTrue(isinstance(room_std_obj, booking_models.RoomStandard))

    def test_null_name(self):
        '''Null Name Creating RoomStandard (Model)'''
        try:
            room_std_obj = self.create_room_standard(name=None)
        except:
            pass
        self.assertRaises(Exception)

    def test_duplicate_room_standard(self):
        '''Duplicate Room Standard Entry'''
        try:
            room_std_obj = self.create_room_standard(name=self.room_std_name)
            room_std_obj2 = self.create_room_standard(name=self.room_std_name)
        except:
            self.assertRaises(Exception)

    def test_str_room_standard(self):
        '''Check Str return in RoomStandard Model'''
        room_std_obj = booking_models.RoomStandard.objects.create(name=self.room_std_name)
        self.assertEqual(room_std_obj.__str__(), room_std_obj.name)

    def test_get_absolute_url(self):
        '''Check Absolute URl in RoomStandard Model'''
        room_std_obj = booking_models.RoomStandard.objects.create(name=self.room_std_name)
        pass

class RoomModelTest(TestCase):

    @classmethod
    def setUp(cls):
        room_std_obj = booking_models.RoomStandard.objects.create(name='Executive')
        room_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.room_data = {
            'name': 'Elgon',
            'room_image': room_image,
            'capacity': 2,
            'room_standard': room_std_obj,
        }
        cls.room_invalid_data = {
            'name': '',
            'room_image': room_image,
            'capacity': 5,
            'room_standard': None,
        }
    def create_room(self,**kwargs):
        room_object = booking_models.Room.objects.create(**kwargs)
        return room_object

    def test_create_room(self):
        '''Create Room on Valid Data'''
        room_obj = self.create_room(**self.room_data)
        self.assertTrue(isinstance(room_obj, booking_models.Room))

    def test_null_room_standard(self):
        '''Dont Create Room on InValid Data'''
        try:
            room_obj = self.create_room(**self.room_data_invalid)
        except:
            pass
        self.assertRaises(Exception)

    def test_duplicates(self):
        '''Duplicates in Room Model'''
        try:
            room_obj = self.create_room(**self.room_data)
            room_obj2 = self.create_room(**self.room_data)
        except:
            self.assertRaises(Exception)
    def test_absolute_url(self):
        '''Room model Absolute Url'''
        room_obj = self.create_room(**self.room_data)
        self.assertEquals(room_obj.get_absolute_url(), reverse('booking:room-detail', kwargs={'pk': room_obj.pk}))

    def test_str_room(self):
        '''str returned in room model'''
        room_obj = self.create_room(**self.room_data)

        self.assertEquals(room_obj.__str__(), room_obj.name)

class BookingTest(TestCase):

    @classmethod
    def setUp(cls):
        user = User.objects.create_user(username='sadio_mane', email='sadiomane@gmail.com', first_name='sadio', last_name='mane', password='p@ssw0rd')
        room_std_obj = booking_models.RoomStandard.objects.create(name='Executive')
        room_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        room_data = {
            'name': 'Elgon',
            'room_image': room_image,
            'capacity': 2,
            'room_standard': room_std_obj,
        }
        room_obj = booking_models.Room.objects.create(**room_data)

        check_in = date(2018, 6, 7)
        check_out = date(2018, 6, 20)
        cls.booking_valid_data = {
            'check_in': check_in,
            'check_out': check_out,
            'room': room_obj,
            'receptionist': user,
        }

        cls.booking_invalid_data = {
            'check_in': None,
            'check_out': None,
            'room': None,
            'receptionist': user,
        }

    def create_booking(self, **kwargs):
        booking = booking_models.Booking.objects.create(**kwargs)
        return booking

    def test_create_booking(self):
        '''Valid data gets processed through Booking model'''
        booking_obj = self.create_booking(**self.booking_valid_data)
        self.assertTrue(isinstance(booking_obj, booking_models.Booking))

    def test_null_fields_booking(self):
        '''Invalid data does not gets processed through Booking model'''
        try:
            booking_obj = self.create_booking(**self.booking_invalid_data)
        except:
            pass
        self.assertRaises(Exception)

    def test_duplicates_booking(self):
        '''Duplicates creating Booking Model'''
        try:
            booking_obj = self.create_booking(**self.booking_valid_data)
            booking_obj2 = self.create_booking(**self.booking_valid_data)
        except:
            self.assertRaises(Exception)

    def test_absolute_url(self):
        '''Booking model Absolute Url'''
        booking_obj = self.create_booking(**self.booking_valid_data)
        self.assertEquals(booking_obj.get_absolute_url(), reverse('booking:booking-detail', kwargs={'pk': booking_obj.pk}))

    def test_str_room(self):
        '''str returned in Booking model'''
        booking_obj = self.create_booking(**self.booking_valid_data)
        booking_str = "%s - %s - %s - %s" % (booking_obj.room.name,booking_obj.check_in, booking_obj.check_out, booking_obj.processed)
        self.assertEquals(booking_obj.__str__(), booking_str)

class TestHotelGuest(TestCase):

    @classmethod
    def setUp(cls):

        user = User.objects.create_user(username='sadio_mane', email='sadiomane@gmail.com', first_name='sadio', last_name='mane', password='p@ssw0rd')
        room_std_obj = booking_models.RoomStandard.objects.create(name='Executive')
        room_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        room_data = {
            'name': 'Elgon',
            'room_image': room_image,
            'capacity': 2,
            'room_standard': room_std_obj,
        }
        room_obj = booking_models.Room.objects.create(**room_data)
        check_in = date(2018, 6, 7)
        check_out = date(2018, 6, 20)
        booking_valid_data = {
            'check_in': check_in,
            'check_out': check_out,
            'room': room_obj,
            'receptionist': user,
        }
        cls.booking_obj = booking_models.Booking.objects.create(**booking_valid_data)

        cls.hotel_guest_data = {
            'full_name': 'kim jong',
            'phone_number': '0605812845',
            'email': 'kimjong@example.com',
        }
        cls.hotel_guest_invalid_data = {
            'full_name': None,
            'phone_number': None,
            'email': 'kimjong@example.com',
        }

    def create_hotel_guest(self, **kwargs):
        hotel_guest_object = booking_models.HotelGuest.objects.create(**kwargs)
        # Add a Many to Many Field Instance
        hotel_guest_object.booking.add(self.booking_obj)
        return hotel_guest_object

    def test_create_hotel_guest(self):
        '''Valid data proceeds to processing in HotelGuest Model'''
        hotel_guest_obj = self.create_hotel_guest(**self.hotel_guest_data)
        self.assertTrue(isinstance(hotel_guest_obj, booking_models.HotelGuest))

    def test_null_fields_hotelguest(self):
        '''Full Name for Hotel Guest must be in the correct format'''
        try:
            hotel_guest_obj = self.create_hotel_guest(**self.hotel_guest_invalid_data)
        except:
            pass
        self.assertRaises(Exception)

    def test_duplicates_hotelguest(self):
        '''Ensure no duplicates occur in HotelGuest Table'''
        try:
            hotel_guest_obj_1 = self.create_hotel_guest(**self.hotel_guest_data)
            hotel_guest_obj_2 = self.create_hotel_guest(**self.hotel_guest_data)
        except:
            pass
        self.assertRaises(Exception)

    def test_absolute_url(self):
        '''Hotel Guest model Absolute Url'''
        hotel_guest_obj = self.create_hotel_guest(**self.hotel_guest_data)
        #self.assertEquals(hotel_guest_obj.get_absolute_url(), re)
        pass

    def test_str_room(self):
        '''str returned in Booking model'''
        hotel_guest_obj = self.create_hotel_guest(**self.hotel_guest_data)
        hotel_guest_str = str('%s - %s' % (hotel_guest_obj.full_name, hotel_guest_obj.phone_number))
        self.assertEquals(hotel_guest_obj.__str__(), hotel_guest_str)
