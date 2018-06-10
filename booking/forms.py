from django import forms
import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from booking import models as booking_models
from django.forms import BaseFormSet

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True)

    def clean(self):
        all_clean_data = super(LoginForm, self).clean()
        username = all_clean_data.get('username')
        password = all_clean_data.get('password')
        username_checker = User.objects.filter(username=username)
        auth_user = authenticate(username=username, password=password)

        if not username_checker :
            self.add_error('username', 'Username don\'t Exist')
            self.add_error('password', '')
        elif username_checker and not auth_user:
            self.add_error('password', 'Wrong Password, Try Again')


class UserForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }
    def clean(self):
        all_clean_data = super(UserForm, self).clean()
        username = all_clean_data.get('username')
        first_name = all_clean_data.get('first_name')
        last_name = all_clean_data.get('last_name')
        email = all_clean_data.get('email')
        password = all_clean_data.get('password')
        confirm_password = all_clean_data.get('confirm_password')
        required_message = "This Field is Required"

        if not username:
            self.add_error('username', required_message)
        if first_name and not re.match(r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$", first_name):
            self.add_error('first_name', 'Invalid Name Format')
        if last_name and not re.match(r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$", last_name):
            self.add_error('last_name', 'Invalid Name Format')
        if not email:
            self.add_error('email', required_message)
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'Another user has this Email')
        if email and not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            self.add_error(None, 'Invalid Email Format')
        if not confirm_password:
            self.add_error('confirm_password', 'Confirm Password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords Don\'t Match')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = booking_models.UserProfile
        fields = ('profile_pic',)
        exclude = ('user',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email')
        labels = {
            'username': 'Username',
            'password': 'Password',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
        }
    def clean(self):
        all_clean_data = super(UserEditForm, self).clean()
        first_name = all_clean_data.get('first_name')
        last_name = all_clean_data.get('last_name')
        email = all_clean_data.get('email')
        required_message = "This Field is Required"

        if first_name and not re.match(r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$", first_name):
            self.add_error('first_name', 'Invalid Name Format')
        if last_name and not re.match(r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$", last_name):
            self.add_error('last_name', 'Invalid Name Format')
        if not email:
            self.add_error('email', required_message)
        if email and not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            self.add_error('email', 'Invalid Email Format')

class RoomForm(forms.ModelForm):
    class Meta:
        model = booking_models.Room
        fields = ('room_image', 'name', 'capacity', 'room_standard')

    def clean(self):
        all_clean_data = super(RoomForm, self).clean()
        name = all_clean_data.get('name')
        capacity = all_clean_data.get('capacity')
        room_standard = all_clean_data.get('room_standard')
        required_message = "This Field is Required"

        if capacity not in range(1,4):
            self.add_error('capacity', "Room Capacity is between [1-3]")

class HotelGuestForm(forms.ModelForm):
    class Meta:
        model = booking_models.HotelGuest
        fields = ('full_name', 'phone_number', 'email')

    def clean(self):
        all_clean_data = super(HotelGuestForm, self).clean()
        full_name = all_clean_data.get('full_name')
        phone_number = all_clean_data.get('phone_number')
        email = all_clean_data.get('email')

        if full_name and not re.match(\
        r"^([a-zA-Z]{2,}\s[a-zA-z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)",\
         full_name):
            self.add_error('full_name', 'Invalid Full Name Format')
        if phone_number and not re.match(\
        r"(\d{3})\D*(\d{3})\D*(\d{4})",\
         phone_number):
            self.add_error('phone_number', 'Invalid Phone Number Format')
        if email and not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            self.add_error('email', 'Invalid Email Format')

        return all_clean_data

class BookingForm(forms.ModelForm):
    class Meta:
        model = booking_models.Booking
        fields = ['check_in', 'check_out', 'room']

    def clean(self):
        all_clean_data = super().clean()
        check_in = all_clean_data.get('check_in')
        check_out = all_clean_data.get('check_out')
        room  = all_clean_data.get('room')
        required_msg = 'This field is required.'
        check_out

        if not check_in:
            self.add_error('check_in', required_msg)
        if not check_out:
            self.add_error('check_out', required_msg)
        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out', 'Enter a Date after Check In')
        if not room:
            self.add_error(None, 'Please Choose a Room through Guests Options')

        return all_clean_data
