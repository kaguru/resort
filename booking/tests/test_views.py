from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
import tempfile
from io import BytesIO
from django.contrib.auth.models import User
from booking import models as booking_models
from booking import forms as booking_forms

class AuthTests(TestCase):

    @classmethod
    def setUp(cls):
        user = User.objects.create(username='sadio_mane', email='sadiomane@gmail.com', first_name='sadio', last_name='mane', password='p@ssw0rd')
        cls.register_details = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'confirm_password': user.password,
        }
        cls.login_credentials = {
            'username': cls.register_details['username'],
            'password':cls.register_details['password'],
        }

    def test_login_view(self):
        '''Create USer Loging Sesion'''
        user = User.objects.get(username=self.login_credentials['username'])
        self.client.force_login(user)
        response_get = self.client.get(reverse_lazy('booking:login'), follow=False)
        response_post = self.client.post(reverse_lazy('booking:login'), self.login_credentials, follow=True)

        self.assertTemplateUsed(response_get, 'registration/login.html')
        self.assertEquals(reverse_lazy('booking:login'), '/booking/accounts/login/')
        self.assertEquals(response_get.status_code, 200)
        self.assertEquals(response_post.status_code, 200)
        self.assertTrue(response_post.context['user'].is_active)
        self.assertTrue(response_post.context['user'].is_authenticated)

    def test_logout_view(self):
        '''Logout User Session'''
        user = User.objects.get(username=self.login_credentials['username'])
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('booking:logout'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(reverse_lazy('booking:logout'), '/booking/accounts/logout/')
        self.assertFalse(response.context['user'].is_active)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_valid_register(self):
        '''Post Registration Detail if form is valid
            and User No Login Session
        '''
        self.client.logout()
        response_get = self.client.get(reverse_lazy('booking:register'), follow=True)
        response_post = self.client.post(reverse_lazy('booking:register'), self.register_details, follow=True)

        self.assertEquals(response_get.status_code, 200)
        self.assertEquals(response_post.status_code, 200)
        self.assertEquals(reverse_lazy('booking:register'), '/booking/accounts/register/')
        self.assertTemplateUsed(response_get, 'registration/register.html')

    def test_auth_register(self):
        '''Dont Post Registration Details if User is Logged In'''
        user = User.objects.get(username=self.login_credentials['username'])
        self.client.force_login(user)
        response_post = self.client.post(reverse_lazy('booking:register'), self.register_details, follow=True)

        self.assertNotEquals(response_post.status_code, 200)


class ProfileTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gdot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }
    def create_user(self, **kwargs):
        user = User.objects.create_user(**kwargs)
        return user

    def test_valid_profile_detail_view(self):
        '''View Profile Detail if Loging Session Exists'''
        user = self.create_user(**self.user_data)
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('booking:profile-detail', kwargs={'pk': user.pk}), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(reverse_lazy('booking:profile-detail', kwargs={'pk': user.pk}), '/booking/accounts/profile-detail/{}'.format(user.pk))
        self.assertTemplateUsed(response, 'booking/profile_detail.html')

    def test_auth_profile_detail_view(self):
        '''Dont View USer Profile if there is no Login Session'''
        user = self.create_user(**self.user_data)
        self.client.logout()
        response = self.client.get(reverse_lazy('booking:profile-detail', kwargs={'pk': user.pk}), follow=True)

    def test_valid_profile_edit_view(self):
        '''Edit User Detail if Form is Valid and Login Session Available'''
        user = self.create_user(**self.user_data)
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('booking:profile-edit', kwargs={'pk': user.pk}), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(reverse_lazy('booking:profile-edit', kwargs={'pk': user.pk}), '/booking/accounts/profile-edit/{}/'.format(user.pk))
        self.assertTemplateUsed(response, 'booking/profile_edit.html')

    def test_auth_profile_edit_view(self):
        '''Dont Edit User Details if no User Login Session'''
        user = self.create_user(**self.user_data)
        self.client.logout()
        response = self.client.get(reverse_lazy('booking:profile-edit', kwargs={'pk': user.pk}), follow=True)

class RoomTests(TestCase):

    @classmethod
    def setUp(cls):
        room_std_obj = booking_models.RoomStandard.objects.create(name='Executive')
        room_image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        cls.room_formset_data = {
            'form-INITIAL_FORMS' : '0' ,
            'form-TOTAL_FORMS' : '1' ,
            'form-MIN_NUM_FORMS': '1',
            'form-0-room_image' : room_image ,
            'form-0-name' : 'Longonot' ,
            'form-0-capacity' : 2,
            'form-0-room_standard' : room_std_obj.pk,
        }

        cls.user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gdot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }

    def create_user(self, **kwargs):
        user = User.objects.create_user(**kwargs)
        return user

    def test_valid_room_create(self):
        '''Valid data gets posted in Room View'''
        user = self.create_user(**self.user_data)
        self.client.force_login(user)
        response_get = self.client.get(reverse('booking:room-create'), self.room_formset_data, follow=False)
        response_post = self.client.post(reverse('booking:room-create'), self.room_formset_data, follow=True)

        self.assertEquals(response_post.status_code, 200)
        self.assertTemplateUsed(response_get, 'booking/room_create.html')
        self.assertEquals(reverse('booking:room-create'), '/booking/room/create/')

    def test_auth_room_create(self):
        '''User has to be logged in to submit room data'''
        self.client.logout()
        response = self.client.post(reverse('booking:room-create'), self.room_formset_data, follow=False)
        self.assertNotEquals(response.status_code, 200)

class BookingViewTest(TestCase):

    @classmethod
    def setUp(cls):
        #room data
        room_std = booking_models.RoomStandard.objects.create(name='Delux')

        room_data = {
            'room_image' : '' ,
            'name' : 'Longonot' ,
            'capacity' : 2,
            'room_standard' : room_std,
        }
        room_obj = booking_models.Room.objects.create(**room_data)

        # Booking Data
        cls.booking_data = {
            'form-INITIAL_FORMS' : '0' ,
            'form-TOTAL_FORMS' : '1' ,
            'form-MIN_NUM_FORMS': '1',
            'form-0-full_name' : 'jamie vardie' ,
            'form-0-phone_number' : '0767893456' ,
            'form-0-email' : 'jamie@example.com',
            'check_in': "12-4-2018",
            'check_out': "14-4-2018",
            'room': room_obj,
        }

        #user Data
        cls.user_data = {
            'username': 'gal_gadot',
            'first_name': 'gal',
            'last_name': 'gdot',
            'email': 'gal@domain.com',
            'password': 'p@ssw0rd',
        }

    def create_user(self, **kwargs):
        user = User.objects.create_user(**kwargs)
        return user

    def test_valid_booking_view(self):
        '''Valid Booking data gets posted in Booking View'''
        user = self.create_user(**self.user_data)
        self.client.force_login(user)
        response_get = self.client.get(reverse('booking:booking-create'), self.booking_data, follow=False)
        response_post = self.client.post(reverse('booking:booking-create'), self.booking_data, follow=True)

        self.assertEquals(response_post.status_code, 200)
        self.assertTemplateUsed(response_get, 'booking/booking-create.html')
        self.assertEquals(reverse('booking:booking-create'), '/booking/create/')

    def test_auth_booking(self):
        '''You have to be logged in to process booking'''
        self.client.logout()
        response_post = self.client.post(reverse('booking:booking-create'), self.booking_data, follow=False)

        self.assertNotEquals(response_post.status_code, 200)
