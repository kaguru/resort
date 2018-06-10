from django.contrib import admin
from booking import models as booking_models
from django.conf.locale.es import formats as es_formats
# Register your models here.

admin.site.register(booking_models.UserProfile)
admin.site.register(booking_models.RoomStandard)
admin.site.register(booking_models.Room)
admin.site.register(booking_models.Booking)
admin.site.register(booking_models.HotelGuest)

#CHANGE DATE FORMAT IN THE ADMIN SECTION
es_formats.DATETIME_FORMAT = "d M Y H:i:s"
es_formats.DATE_FORMAT = "d M Y"
