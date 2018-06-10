from django.urls import reverse
from django.forms import inlineformset_factory
from django import views as django_views
from django.views import generic as django_generic_views
from django.views.generic import edit as django_edit_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from booking import forms as booking_forms
from booking import models as booking_models

# Create your views here.

class ProfileDetailView(LoginRequiredMixin, django_generic_views.DetailView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'booking/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileEditView(LoginRequiredMixin, django_edit_views.UpdateView):
    model = booking_models.User
    fields=('first_name', 'last_name', 'email')
    profile_form =  booking_forms.UserProfileForm
    template_name = 'booking/profile_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = super(ProfileEditView, self).get_object()
        try:
            userprofile_inst = booking_models.UserProfile.objects.get(user=self.object)
            profile_form = self.profile_form(request.POST, request.FILES, instance=userprofile_inst)
        except:
            profile_form = self.profile_form(request.POST, request.FILES)

        context =super(ProfileEditView, self).get_context_data(**kwargs)
        context['profile_form'] = profile_form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = super(ProfileEditView, self).get_object()
        try:
            userprofile_inst = booking_models.UserProfile.objects.get(user=self.object)
            profile = self.profile_form(request.POST, request.FILES, instance=userprofile_inst)
            if 'profile_pic' in self.request.FILES:
                profile.profile_pic = self.request.FILES.get('profile_pic')
            profile.save()
        except:
            pass
        return super(ProfileEditView, self).post(request, **kwargs)

    def get_success_url(self):
        return reverse('booking:profile-detail', kwargs={'pk': self.request.user.pk })
