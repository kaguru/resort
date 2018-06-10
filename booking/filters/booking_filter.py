from django.db.models import Q
from django.db.models import Q
import django_filters
from booking import models as booking_models
from django.utils import timezone

class BookingFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='general_search_queryset')
    class Meta:
        model = booking_models.Booking
        fields = []

    def general_search_queryset(self, value):
        room_objects = booking_models.Booking.objects.filter(
        Q(check_in__contains = value)\
        | Q(check_out__contains = value)\
        | Q(room__name__contains = value)\
        | Q(receptionist__username__contains = value))

        return room_objects

    def room_standards_queryset(value):
        room_objects = booking_models.Booking.objects.filter(\
        Q(room_standard__name = value))
        return room_objects

    def general_queryset(self, queryset, name, value):
        return queryset.filter(self.general_search_queries(value))
