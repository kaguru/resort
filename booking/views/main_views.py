from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
from django.forms import BaseFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django import views as django_views
from django.views import generic as django_generic_views
from django.views.generic import edit as django_edit_views
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from booking import forms as booking_forms
from django.db.models import Q
from booking import models as booking_models
from django.contrib.auth.models import User
from booking.filters import room_filter, booking_filter, guest_filter
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Room BaseFormset
class RoomBaseFormset(BaseFormSet):
    def clean(self):
        '''Validation of Room Formset'''
        if any(self.errors):
            return
        else:
            names_list = []
            for form in self.forms:
                name = form.cleaned_data.get('name')
                if name in names_list:
                    return form.add_error('name', 'Room names should be Unique')
                names_list.append(name)

# Booking BaseFormset
class HotelGuestBaseFormset(BaseFormSet):
    def clean(self):
        '''Validation of Booking Formset'''
        if any(self.errors):
            return

        full_name_list = []
        for form in self.forms:
            full_name = form.cleaned_data.get('full_name')
            if full_name in full_name_list:
                form.add_error('full_name', 'Duplicates in Full Names')
            full_name_list.append(full_name)
# Create your views here.
class IndexView(django_views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'booking/index.html')

# Room CreateView
class RoomCreateView(LoginRequiredMixin, django_edit_views.CreateView):
    form_class = booking_forms.RoomForm
    template_name = 'booking/room_create.html'
    RoomsFormset = formset_factory(booking_forms.RoomForm, formset=RoomBaseFormset, extra=0, min_num=1, max_num=5,can_order=False, can_delete=False)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = None
        rooms_formset = self.RoomsFormset(request.POST, request.FILES)
        if rooms_formset.is_valid():
            return self.form_valid(rooms_formset)
        else:
            return self.form_invalid()

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs);
        if self.request.POST:
            context['rooms_formset'] = self.RoomsFormset(self.request.POST)
        else:
            context['rooms_formset'] = self.RoomsFormset()
        context['rooms_list'] = booking_models.Room.objects.all()

        return context

    def form_valid(self, rooms_formset):
        room_obj = None
        for form in rooms_formset:
            room_obj = form.save()
        messages.success(self.request, 'Successfully Saved Room')
        return HttpResponseRedirect(self.get_absolute_url())

    def form_invalid(self):
        messages.error(self.request, 'Correct Errors in the Form')
        return self.render_to_response(self.get_context_data())

    def get_absolute_url(self):
        return reverse('booking:room-list')

# List All Rooms Search by multiple fields
class RoomListView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Room
    template_name = 'booking/room_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        name = request.GET.get('name')

        if name:
            return HttpResponseRedirect(reverse('booking:room-search', kwargs={'name': name}))
        else:
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['search_form'] = room_filter.RoomsFilter(self.request.GET).form

        return context

# List All Rooms Search by multiple fields
class RoomSearchView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Room
    filter_class = room_filter.RoomsFilter
    template_name = 'booking/room_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        name = kwargs.get('name')
        my_query_set = None

        if name:
            my_query_set = self.filter_class().general_search_queryset(name)
        else:
            my_query_set = self.object_list

        context = self.get_context_data(object_list=my_query_set)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(RoomSearchView, self).get_context_data(**kwargs)
        context['search_form'] = self.filter_class(self.request.GET).form
        return context

class GuestListView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.HotelGuest
    filter_class = guest_filter.GuestsFilter
    template_name = 'booking/guest_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.filter_class().general_search_queryset('')
        context = self.get_context_data(object_list=self.object_list)
        name = request.GET.get('name')

        if name:
            return HttpResponseRedirect(reverse('booking:guest-search', kwargs={'name': name}))
        else:
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GuestListView, self).get_context_data(**kwargs)
        context['search_form'] = room_filter.RoomsFilter(self.request.GET).form

        return context

# List All Rooms Search by multiple fields
class GuestSearchView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.HotelGuest
    filter_class = guest_filter.GuestsFilter
    template_name = 'booking/guest_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        name = kwargs.get('name')
        my_query_set = None

        if name:
            my_query_set = self.filter_class().general_search_queryset(name)
        else:
            my_query_set = self.object_list

        context = self.get_context_data(object_list=my_query_set)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GuestSearchView, self).get_context_data(**kwargs)
        context['search_form'] = self.filter_class(self.request.GET).form
        return context

# Filter Rooms by RoomStandard
class RoomStandardFilterView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Room
    filter_class = room_filter.RoomsFilter
    template_name = 'booking/room_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = []
        room_std_name = kwargs['name']
        custom_queryset = self.filter_class.room_standards_queryset(room_std_name)
        context = self.get_context_data(object_list=custom_queryset)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
            context = super(RoomStandardFilterView, self).get_context_data(**kwargs)
            context['search_form'] = self.filter_class(self.request.GET).form

            return context

# Filter Rooms by Booked
class StatusFilterView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Room
    filter_class = room_filter.RoomsFilter
    template_name = 'booking/room_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        status = kwargs.get('status')
        my_query_set = None

        if status == 'True':
            my_query_set = self.filter_class().booked_rooms_queryset()
        elif status == 'False':
            my_query_set = self.filter_class().vacant_rooms_queryset()
        elif status == 'ending':
            my_query_set = self.filter_class().ending_rooms_queryset()
        else:
            my_query_set = self.object_list

        context = self.get_context_data(object_list=my_query_set)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(StatusFilterView, self).get_context_data(**kwargs)
        context['search_form'] = self.filter_class(self.request.GET).form
        return context

 # Room Detail View
class RoomDetailView(LoginRequiredMixin, django_generic_views.DetailView):
    model = booking_models.Room
    template_name = 'booking/room_detail.html'

# Room Edit View
class RoomEditView(LoginRequiredMixin, django_generic_views.UpdateView):
    model = booking_models.Room
    form_class = booking_forms.RoomForm
    template_name = 'booking/room_edit.html'

# Delete Booking
class RoomDeleteView(LoginRequiredMixin, django_edit_views.DeleteView):
    model = booking_models.Room
    template_name = 'booking/room_delete.html'
    success_url = reverse_lazy('booking:room-list')

# Booking View
class BookingCreateView(LoginRequiredMixin ,django_edit_views.CreateView):
    form_class = booking_forms.BookingForm
    template_name = 'booking/booking-create.html'
    HotelGuestFormset = formset_factory(booking_forms.HotelGuestForm, formset=HotelGuestBaseFormset, extra=0, max_num=3, min_num=1, can_order=False, can_delete=False)
    vacant_rooms_filter_class = room_filter.RoomsFilter

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        hotel_guest_formset = self.HotelGuestFormset(request.POST, request.FILES)
        new_booking_form = self.form_class(request.POST, request.FILES)

        if new_booking_form.is_valid() and hotel_guest_formset.is_valid():
            return self.form_valid(new_booking_form, hotel_guest_formset)
        else:
            return self.form_invalid()

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        context['vacant_rooms'] = self.vacant_rooms_filter_class().vacant_rooms_queryset()

        if self.request.POST:
            context['new_booking_form'] = self.form_class(self.request.POST)
            context['hotel_guest_formset'] = self.HotelGuestFormset(self.request.POST)
        else:
            context['new_booking_form'] = self.get_form_class()
            context['hotel_guest_formset'] = self.HotelGuestFormset()

        return context

    def form_valid(self, new_booking_form, hotel_guest_formset):
        for form in hotel_guest_formset:
            obj = form.save(commit=False)
            if form.cleaned_data.get('full_name') and form.cleaned_data.get('phone_number'):
                booking_obj = new_booking_form.save(commit=False)
                booking_obj.receptionist = self.request.user
                booked_room = new_booking_form.cleaned_data.get('room')
                booked_room.last_booked = timezone.now()
                booked_room.book_out = new_booking_form.cleaned_data.get('check_out')
                booked_room.save()
                booking_obj.save()
                try:
                    user = booking_models.HotelGuest.objects.get(phone_number=form.cleaned_data.get('phone_number'))
                    user.full_name = form.cleaned_data.get('full_name')
                    user.email = form.cleaned_data.get('email')
                    user.booking.add(booking_obj)
                    user.save()
                except booking_models.HotelGuest.DoesNotExist:
                    obj.full_name = form.cleaned_data.get('full_name')
                    obj.phone_number = form.cleaned_data.get('phone_number')
                    obj.email = form.cleaned_data.get('email')
                    obj.save()
                    obj.booking.add(booking_obj)
            else:
                return self.form_invalid()

        messages.success(self.request, 'Successfully Reserved Booking')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self):
        messages.error(self.request, 'Correct Errors in the Form')
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse('booking:booking-list')

@login_required
def filter_rooms(request):
    capacity = request.GET.get('capacity', None)
    vacant_rooms_queryset = room_filter.RoomsFilter(request.GET).vacant_rooms_queryset()


    filtered_data = vacant_rooms_queryset.filter(\
    Q(capacity = capacity)\
    ).values('id', 'name','room_standard__name', 'room_standard__id','capacity')
    # later to replace with vacant queryset
    data = {
        'results': list(filtered_data)
    }

    return JsonResponse(data)

#Booking View
class BookingsList(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Booking
    template_name = 'booking/booking-list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        name = request.GET.get('name')

        if name:
            return HttpResponseRedirect(reverse('booking:booking-search', kwargs={'name': name}))
        else:
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(BookingsList, self).get_context_data(**kwargs)
        context['search_form'] = booking_filter.BookingFilter(self.request.GET).form

        return context

# List All Bookings by Search by multiple fields
class BookingsSearchView(LoginRequiredMixin, django_generic_views.ListView):
    model = booking_models.Booking
    filter_class = booking_filter.BookingFilter
    template_name = 'booking/booking-list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        name = kwargs.get('name')
        my_query_set = booking_models.Booking.objects.none()

        if name:
            my_query_set = self.filter_class().general_search_queryset(name)
        else:
            my_query_set = self.object_list

        context = self.get_context_data(object_list=my_query_set)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(BookingsSearchView, self).get_context_data(**kwargs)
        context['search_form'] = self.filter_class(self.request.GET).form
        return context

#Single Booking Detail View
class BookingDetails(LoginRequiredMixin, django_generic_views.DetailView):
    model = booking_models.Booking
    template_name = 'booking/booking_detail.html'

# Delete Booking
class BookingDelete(LoginRequiredMixin, django_edit_views.DeleteView):
    model = booking_models.Booking
    template_name = 'booking/delete.html'
    success_url = reverse_lazy('booking:bookings')

# Error views 404/ 500
def handler404(request):
    return render(request, 'booking/404.html')


def handler500(request):
    return render(request, 'booking/500.html')

class RoomStandardCreateView(LoginRequiredMixin, django_generic_views.CreateView):
    model = booking_models.RoomStandard
    fields = ('name',)
    template_name = 'booking/room_standard_create.html'

    def get_success_url(self):
        return reverse('booking:room-create')

# Delete Booking
class RoomStandardDeleteView(LoginRequiredMixin, django_edit_views.DeleteView):
    model = booking_models.RoomStandard
    template_name = 'booking/delete.html'
    success_url = reverse_lazy('booking:room-list')
