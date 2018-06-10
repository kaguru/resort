from django.test import TestCase
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
from booking import forms as booking_forms
from booking import models as booking_models
from booking.views import main_views
from django.contrib.auth.models import User
from io import BytesIO
import tempfile
from datetime import date

class TestLoginForm(TestCase):

    @classmethod
    def setUp(cls):
        user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gadot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }
        cls.login_data = {
            'username': user_data['username'],
            'password': user_data['password'],
        }
        cls.login_data_invalid = {
            'username': user_data['username'],
            'password': 'Wr0ngP@ss',
        }
        cls.user = User.objects.create_user(**user_data)

    def process_login_form(self, data):
        form = booking_forms.LoginForm(data=data)
        return form

    def test_valid_login_form(self):
        '''Valid Data Should be submitted in Login Form'''
        form = self.process_login_form(data=self.login_data)
        self.assertTrue(form.is_valid())

    def test_wrong_password(self):
        '''Wrong Password in Login Form'''
        right_pass = self.user.password
        wrong_pass = self.login_data_invalid['password']
        form = self.process_login_form(data=self.login_data_invalid)
        self.assertNotEquals(right_pass, wrong_pass)
        self.assertFalse(form.is_valid())

class UserFormTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.register_data = {
            'username': 'ander_herera',
            'first_name': 'ander',
            'last_name': 'herera',
            'email': 'ander@domain.com',
            'password': '@Mys3cr3t',
            'confirm_password': '@Mys3cr3t',
        }
        cls.register_invalid_data = {
            'username': 'ander_herera',
            'first_name': '1234',
            'last_name': '5678',
            'email': 'invalidemail',
            'password': '@Mys3cr3t',
            'confirm_password': '@nothers3cr3t',
        }
        cls.user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gadot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }

    def process_user_form(self, data):
        '''Process Login Form '''
        form = booking_forms.UserForm(data)
        return form

    def test_valid_user_form(self):
        '''Valid Data gets Submitted in UserForm'''
        form = self.process_user_form(data=self.register_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        '''Invalid Data shouldn't be submitted in USer Form'''
        form = self.process_user_form(data=self.register_invalid_data)
        self.assertRaises(Exception)

    def test_duplicate_username(self):
        '''User data submitted in User Form should be unique to the Existing'''
        user = User.objects.create_user(**self.user_data)
        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'confirm_password': user.password,
        }
        form = self.process_user_form(data=data)
        self.assertFalse(form.is_valid())

class UserProfileFormTest(TestCase):

    @classmethod
    def setUp(cls):
        user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gadot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }
        cls.user = User.objects.create_user(**user_data)

    def test_valid_userprofile_form(self):
        '''Valid UserProfile form gets submitted'''
        user = self.user
        profile_pic = BytesIO(b'my_profile_image_binary_data')
        data = {
            'user': user.pk,
            'profile_pic': profile_pic,
        }
        form = booking_forms.UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

class ProfileEditFormTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.edit_data = {
            'username': 'dele_alli',
            'first_name': 'dele',
            'last_name': 'alli',
            'email': 'dele@domain.com',
        }

        cls.edit_invalid_data = {
            'username': 'dele_alli',
            'first_name': '123',
            'last_name': '456',
            'email': 'invalidmail',
        }
    def process_userprofile_edit_form(self, data):
        form = booking_forms.UserEditForm(data=data)
        return form

    def test_valid_user_edit_form(self):
        '''Valid Data gets Submitted in User Edit Form'''
        form = self.process_userprofile_edit_form(data=self.edit_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_edit_form(self):
        '''Invalid Data shouldn't be submitted in User Edit Form'''
        form = self.process_userprofile_edit_form(data=self.edit_invalid_data)
        self.assertRaises(Exception)

class RoomFormsetTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.RoomsFormset = formset_factory(booking_forms.RoomForm, extra=0, min_num=1, can_order=True, can_delete=True)
        room_std = booking_models.RoomStandard.objects.create(name='Delux')
        room_image = BytesIO(b'room_image_binary_data')

        cls.room_formset_data = {
            'form-INITIAL_FORMS' : '0' ,
            'form-TOTAL_FORMS' : '1' ,
            'form-MIN_NUM_FORMS': '1',
            'form-0-room_image' : room_image ,
            'form-0-name' : 'Longonot' ,
            'form-0-capacity' : 2,
            'form-0-room_standard' : room_std.pk,
        }

        cls.room_no_room_std_data = {
            'form-INITIAL_FORMS' : '0' ,
            'form-TOTAL_FORMS' : '1' ,
            'form-MIN_NUM_FORMS': '1',
            'form-0-room_image' : room_image ,
            'form-0-name' : 'Longonot' ,
            'form-0-capacity' : 2,
            'form-0-room_standard' : '',
        }
        cls.room_capacity_out_of_range = {
            'form-INITIAL_FORMS' : '0' ,
            'form-TOTAL_FORMS' : '1' ,
            'form-MIN_NUM_FORMS': '1',
            'form-0-room_image' : room_image ,
            'form-0-name' : 'Longonot' ,
            'form-0-capacity' : 10,
            'form-0-room_standard' : room_std.pk,
        }
    def process_room_formset(self, data):
        formset = self.RoomsFormset(data=data)
        return formset

    def test_valid_room_formset(self):
        '''Valid data through Room Form gets submitted'''
        form = self.process_room_formset(self.room_formset_data)
        self.assertTrue(form.is_valid())

    def test_room_standard(self):
        '''Room must have a slug and RoomStandard Instance'''
        form = self.process_room_formset(self.room_no_room_std_data)
        self.assertRaises(Exception)

    def test_room_capacity(self):
        '''Check Room Capacity Range'''
        form = self.process_room_formset(self.room_capacity_out_of_range)
        self.assertFalse(form.is_valid())

class HotelGuestTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.guest_valid_data = {
            'full_name': 'jamie vardy',
            'phone_number': '0763345678',
            'email': 'jamie@example.com',
        }
        cls.guest_invalid_formats_data = {
            'full_name': 'jamie',
            'phone_number': '1234',
            'email': 'jamie@example.com',
        }
        cls.guest_blank_data = {
            'full_name': '',
            'phone_number': '',
            'email': '',
        }

    def process_guest_form(self, data):
        form = booking_forms.HotelGuestForm(data=data)
        return form

    def test_submit_form(self):
        '''Valid data in Hotel Guest form gets submitted'''
        form = self.process_guest_form(self.guest_valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data_fields_formats(self):
        '''Invalid data format does not get submitted'''
        form = self.process_guest_form(self.guest_invalid_formats_data)
        self.assertFalse(form.is_valid())

    def test_blank_fields(self):
        '''Blank fullname and phone data format does not get submitted'''
        form = self.process_guest_form(self.guest_blank_data)
        self.assertFalse(form.is_valid())

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
        cls.booking_valid_data = {
            'check_in': "12-4-2018",
            'check_out': "14-4-2018",
            'room': room_obj.pk,
            'receptionist': user.pk,
        }
        cls.booking_invalid_dates_format_data = {
            'check_in': "2018-12-4",
            'check_out': "2018-14-4",
            'room': room_obj.pk,
            'receptionist': user.pk,
        }
        cls.check_out_less_in_data = {
            'check_in': "14-4-2018",
            'check_out': "12-4-2018",
            'room': room_obj.pk,
            'receptionist': user.pk,
        }
        cls.booking_blank_room_data = {
            'check_in': "12-4-2018",
            'check_out': "14-4-2018",
            'room': None,
            'receptionist': user.pk,
        }

    def process_booking_form(self, data):
        form_instance = booking_forms.BookingForm(data=data)
        return form_instance

    def test_booking_valid_submit(self):
        '''Test valid data get submitted through booking form'''
        form = self.process_booking_form(self.booking_valid_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_booking_invalid_date_format(self):
        '''Invalid dates dont get submitted'''
        form = self.process_booking_form(self.booking_invalid_dates_format_data)
        self.assertFalse(form.is_valid())

    def test_check_out_to_check_in(self):
        '''Check out date should be more than check in'''
        form = self.process_booking_form(self.check_out_less_in_data)
        self.assertFalse(form.is_valid())

    def test_blank_room(self):
        '''Form with no room selected dont get submitted'''
        form = self.process_booking_form(self.booking_blank_room_data)
        self.assertFalse(form.is_valid())
