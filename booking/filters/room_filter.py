from django.db.models import Q
import django_filters
from booking import models as booking_models
from django.utils import timezone

class RoomsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='general_search_queryset')
    class Meta:
        model = booking_models.Room
        fields = []

    def general_search_queryset(self, value):
        room_objects = booking_models.Room.objects.filter(
        Q(name__contains = value)\
        | Q(room_standard__name__contains = value)\
        | Q(capacity__contains = value)\
        | Q(book_out__contains = value))

        return room_objects

    def room_standards_queryset(value):
        room_objects = booking_models.Room.objects.filter(\
        Q(room_standard__name = value))
        return room_objects

    def vacant_rooms_queryset(self):
        date_now = timezone.now().date()
        time_now = timezone.now().time().strftime("%H")
        room_objects = None

        if int(time_now) >= 9: #change to 9 later
            room_objects = \
            Q(book_out = date_now)\
            | Q(book_out__lt = date_now )\
            | Q(book_out = None )
        else :
            room_objects = \
            Q(book_out__lt = date_now )\
            | Q(book_out = None )

        return booking_models.Room.objects.filter(room_objects)

    def vacant_rooms_raw_queryset(self):
        date_now = timezone.now().date()
        time_now = timezone.now().time().strftime("%H")
        raw_queryset = None

        if int(time_now) >= 9: #change to 9 later
            raw_queryset = \
            Q(book_out = date_now)\
            | Q(book_out__lt = date_now )\
            | Q(book_out = None )
        else :
            raw_queryset = \
            Q(book_out__lt = date_now )\
            | Q(book_out = None )

        return raw_queryset

    def ending_rooms_queryset(self):
        date_now = timezone.now().date()
        time_now = timezone.now().time().strftime("%H")

        if int(time_now) <9: #change to 9am later on
            room_objects = \
            Q(book_out = date_now)
            return booking_models.Room.objects.filter(room_objects)
        else :
            return booking_models.Room.objects.none()

    def booked_rooms_queryset(self):
        date_now = timezone.now().date()
        time_now = timezone.now().time().strftime("%H")
        room_objects = None

        if int(time_now) <9: #change to 9am later on
            room_objects = \
            Q(book_out = date_now)\
            | Q(book_out__gt = date_now)
        else :
            room_objects = \
            Q(book_out__gt = date_now)

        return booking_models.Room.objects.filter(room_objects)

    def booked_rooms_raw_queryset(self):
        date_now = timezone.now().date()
        time_now = timezone.now().time().strftime("%H")
        raw_queryset = None

        if int(time_now) <9: #change to 9am later on
            raw_queryset = \
            Q(book_out = date_now)\
            | Q(book_out__gt = date_now)
        else :
            raw_queryset = \
            Q(book_out__gt = date_now)

        return raw_queryset

    def general_queryset(self, queryset, name, value):
        return queryset.filter(self.general_search_queries(value))
