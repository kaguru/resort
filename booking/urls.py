"""Booking Url Patterns
"""
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from booking.views import (\
main_views as booking_main_views\
,auth_views as booking_auth_views\
,profile_views as booking_profile_views\
,dashboard_views as booking_dashboard_views\
,statistics_views as booking_stats_views)

def get_url_processor(request):
    name = request.GET.get('')
    return name

app_name = 'booking'

def dd(self):
    name = request.GET.get('name')

urlpatterns = [
    path('', booking_main_views.BookingCreateView.as_view(), name='index'),
    path('create/', booking_main_views.BookingCreateView.as_view(), name='booking-create'),
    path('list/', booking_main_views.BookingsList.as_view(), name='booking-list'),
    path('search/<slug:name>', booking_main_views.BookingsSearchView.as_view(), name='booking-search'),
    path('details/<int:pk>/', booking_main_views.BookingDetails.as_view(), name='booking-detail'),
    path('delete/<int:pk>/', booking_main_views.BookingDelete.as_view(), name='booking-delete'),
    path('json/vacant/rooms/', booking_main_views.filter_rooms, name='vacant-rooms-filter'),
    path('dashboard/', booking_dashboard_views.dashboard_view, name='dashboard'),
    path('statistics/', booking_stats_views.booking_stats_view, name='statistics'),
    path('accounts/logout/', booking_auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', booking_auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', booking_auth_views.RegisterView.as_view(), name='register'),
    path('accounts/profile-detail/<int:pk>', booking_profile_views.ProfileDetailView.as_view(), name='profile-detail'),
    path('accounts/profile-edit/<int:pk>/', booking_profile_views.ProfileEditView.as_view(), name='profile-edit'),
    path('room/create/', booking_main_views.RoomCreateView.as_view(), name='room-create'),
    path('room/detail/<int:pk>/', booking_main_views.RoomDetailView.as_view(), name='room-detail'),
    path('room/edit/<int:pk>/', booking_main_views.RoomEditView.as_view(), name='room-edit'),
    path('room/delete/<int:pk>/', booking_main_views.RoomDeleteView.as_view(), name='room-delete'),
    path('room/list/', booking_main_views.RoomListView.as_view(), name='room-list'),
    path('room/search/<slug:name>/', booking_main_views.RoomSearchView.as_view(), name='room-search'),
    path('room-standard/create/', booking_main_views.RoomStandardCreateView.as_view(), name='room-standard-create'),
    path('room-standard/delete/<int:pk>/', booking_main_views.RoomStandardDeleteView.as_view(), name='room-standard-delete'),
    path('guest/list/', booking_main_views.GuestListView.as_view(), name='guest-list'),
    path('guest/search/<slug:name>/', booking_main_views.GuestSearchView.as_view(), name='guest-search'),
    path('room/list/room_standard/<slug:name>/',booking_main_views.RoomStandardFilterView.as_view(), name='room-room_std_filter'),
    path('room/booked/<slug:status>', booking_main_views.StatusFilterView.as_view(), name='room-status_filter'),
]
