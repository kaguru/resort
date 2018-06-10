from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from uuid import uuid4
import os
from django.utils import timezone

from django.contrib.auth.models import User

#rename profile picture filename
def path_and_rename_pics(instance, filename):
    upload_to = 'profile_pics'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)

    # Further Information about User
    profile_pic = models.ImageField(upload_to=path_and_rename_pics, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('booking:profile-detail', kwargs={'pk': self.user.pk} )

class RoomStandard(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False, unique=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str('%s' % (self.name))

class Room(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    room_image = models.FileField(upload_to='room_images', blank=True, null=True)
    capacity = models.IntegerField(blank=False, null=False)
    room_standard = models.ForeignKey(RoomStandard, on_delete=models.SET_NULL, blank=False, null=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    last_booked = models.DateTimeField(null=True, blank=True)
    book_out = models.DateField(null=True, blank=True)

    @property
    def booked(self):
        '''Create a booked Field with respect to bookout '''
        if self.book_out:
            todays_date = timezone.now().date()
            book_out_date = self.book_out
            str_time_now = timezone.now().time().strftime('%H')
            time_now = int(str_time_now)

            if book_out_date > todays_date:
                    return True
            elif book_out_date == todays_date:
                if time_now < 9: #change to 9 later
                    return 'ending'
                else:
                    return False
            elif book_out_date < todays_date:
                return False
        else:
            return False

    def __str__(self):
        return str('%s' % (self.name))

    def get_absolute_url(self):
        return reverse('booking:room-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ('book_out', '-created')

class Booking(models.Model):
    check_in = models.DateField(blank=True, null=False)
    check_out = models.DateField(blank=True, null=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=False, null=True)
    receptionist = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    processed = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-processed',)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.room.name, self.check_in, self.check_out, self.processed)

    def get_absolute_url(self):
        return reverse('booking:booking-detail', kwargs={'pk': self.pk})


class HotelGuest(models.Model):
    full_name = models.CharField(max_length=30, blank = False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(max_length=50,blank=True, null=False, validators=[
        EmailValidator(
            message="Enter a valid Email",
            code="invalid Email"
        )
    ])
    processed = models.DateTimeField(default=timezone.now)
    booking = models.ManyToManyField(Booking)

    class Meta:
        ordering = ('processed',)

    def __str__(self):
        return str('%s - %s' % (self.full_name,self.phone_number))

    def get_absolute_url(self):
        pass
