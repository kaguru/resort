import json
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Count, Avg, Q, F
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View

from booking.models import Room, RoomStandard, Booking, HotelGuest
from booking.filters import room_filter

@login_required
def booking_stats_view(request):
    vacant_raw_qs = room_filter.RoomsFilter(request).vacant_rooms_raw_queryset()
    booked_raw_qs = room_filter.RoomsFilter(request).booked_rooms_raw_queryset()
    dataset = Room.objects \
        .values('room_standard__name') \
        .annotate(\
                booked_count=Count('room_standard', filter=booked_raw_qs)\
                ,vacant_count=Count('room_standard', filter=vacant_raw_qs))\
        .order_by('room_standard__name')

    booked_rooms_data = []
    vacant_rooms_data = []
    pie_booked_data = []
    room_standards = []

    for entry in dataset:
        standard = entry['room_standard__name']
        room_standards.append(standard)
        booked_rooms_data.append(entry['booked_count'])
        vacant_rooms_data.append(entry['vacant_count'])
        pie_booked_data.append({'name': standard, 'y': entry['booked_count'] })

    booked_rooms = {
        'type': 'column',
        'name': 'Booked',
        'data': booked_rooms_data,
        'color': '#1BA714'
    }

    not_booked_rooms = {
        'type': 'column',
        'name': 'Vacant',
        'data': vacant_rooms_data,
        'color': '#D71A36'
    }

    booked_pie = {
        'type': 'pie',
        'plotBackgroundColor': 'null',
        'plotBorderWidth': 'null',
        'plotShadow': 'false',
        'name': 'Room Standard',
        'colorByPoint': 'true',
        'sliced': 'true',
        'selected': 'true',
        'data': pie_booked_data,
        'size': 250,
        'showInLegend': 'false',
        'dataLabels': {
            'enabled': 'false'
        }
    }

    pie_chart_data = {
        'title': {
            'text': 'Booked Rooms By Room Standards Pie Chart '
        },
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'chart': {
            'options3d': {
        		'enabled': True,
                'alpha': 60,
                'beta': 0,
            },
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': 'true',
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': 'true',
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
                    'style': {
                        'color': "(Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'",
                    }
                },
                'depth': 10,
            }
        },
        'series': [booked_pie]
    }

    column_chart_data = {
        'title': {
            'text': 'Room Bookings By Room Standard Column Chart'
        },
        'xAxis': {
            'title': {
                'text': 'ROOM STANDARDS'
            },
            'categories': room_standards,
            'gridLineWidth': 0,
        },
        'yAxis': {
            'title': {
                'text': 'BOOKINGS'
            },
            'gridLineWidth': 1
        },
        'plotOptions': {
            'column': {
                'borderRadius': 5,
            }
        },
        'chart': {
            'options3d': {
            'enabled': 'true',
            'alpha': 5,
            'beta': 15,
            'depth': 50,
            'viewDistance': 25
        }
        },
        'series': [booked_rooms, not_booked_rooms]
    }

    dump_pie_chart = json.dumps(pie_chart_data)
    dump_column_chart = json.dumps(column_chart_data)
    context = {
        'pie_chart': dump_pie_chart,
        'column_chart': dump_column_chart,
        'dataset': dataset,
        'room_standards': list(room_standards)
        }
    return render(request, 'booking/statistics.html', context)
