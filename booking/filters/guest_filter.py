from django.db.models import Q, Count
import django_filters
from booking import models as booking_models
from django.utils import timezone

class GuestsFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='general_search_queryset')
    class Meta:
        model = booking_models.HotelGuest
        fields = []

    def general_search_queryset(self, value):
        qs_raw = booking_models.HotelGuest.objects.filter(
        Q(full_name__contains = value)\
        | Q(phone_number__contains = value)\
        | Q(email__contains = value)\
        | Q(processed__contains = value))\
        .annotate(
            total_bookings=Count('booking__pk')).order_by('-total_bookings', '-processed')

        return qs_raw

    def general_queryset(self, queryset, name, value):
        return queryset.filter(self.general_search_queries(value))
