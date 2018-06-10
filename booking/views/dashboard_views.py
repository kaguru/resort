from django.shortcuts import render
from django.db.models import Count, Avg, Max, Q, F
from django.contrib.auth.decorators import login_required
from booking.filters import room_filter
from booking.models import Room, RoomStandard, Booking, HotelGuest
from booking import models as booking_models

@login_required
def dashboard_view(request):
    vacant_qs = room_filter.RoomsFilter(request).vacant_rooms_queryset()
    booked_qs = room_filter.RoomsFilter(request).booked_rooms_queryset()

    booked_data = booked_qs\
        .aggregate(\
            booked_count =Count('pk', distinct=True)\
            ,active_bookings =Count('booking__pk', distinct=True)\
            ,active_guests = Count('booking__hotelguest__pk', distinct=True)\
            ,latest_booking = Max('booking__processed')\
            ,latest_room = Max('created')\
            ,latest_guest = Max('booking__hotelguest__processed'))

    room_count = booking_models.Room.objects\
        .aggregate(\
            total_rooms = Count('pk', distinct=True))

    bookings_count = booking_models.Booking.objects\
        .aggregate(\
            total_bookings = Count('pk', distinct=True))

    guests_count = booking_models.HotelGuest.objects\
        .aggregate(\
            total_guests = Count('pk', distinct=True))

    context = {
                'booked_data': booked_data,
                'guests_count': guests_count,
                'room_count': room_count,
                'bookings_count': bookings_count,
            }

    return render(request, 'booking/dashboard.html', context)
