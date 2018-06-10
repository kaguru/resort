from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import edit as django_edit_views
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError


from booking import forms as booking_forms

class LoginView(LoginView):
    template_name = 'registration/login.html'
    login_form =  booking_forms.LoginForm
    next_page_global = '/'

    def get(self, request, *args, **kwargs):
        global next_page_global
        next_page  = request.GET.get('next')
        if next_page:
            next_page_global = next_page
        else:
            next_page_global = '/'
        print ("YYYY--{}".format(next_page))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = None
        login_form = self.login_form(self.request.POST)

        if login_form.is_valid():
            return self.form_valid(login_form)
        else:
            return self.form_invalid()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.login_form(self.request.POST)
        else:
            context['form'] = self.login_form()
        return context

    def form_valid(self, login_form):
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        global next_page_global

        if user:
            if user.is_active:
              login(self.request, user)
            else:
              return HttpResponse("Account Not Active")
        else:
            messages.error(self.request, 'Invalid Login Credentials')
            return self.form_invalid()

        messages.success(self.request, 'Successfully Logged In')
        return HttpResponseRedirect(next_page_global)

    def form_invalid(self):
        return self.render_to_response(self.get_context_data())


class LogoutView(LoginRequiredMixin, LogoutView):
    def get_next_page(self):
        return reverse('booking:login')

class RegisterView(django_edit_views.CreateView):
    form_class = booking_forms.UserForm
    profile_form =  booking_forms.UserProfileForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(self.request, "There\'s an Active Login Session")
            return self.render_to_response(self.get_context_data())
        else:
            return self.render_to_response(self.get_context_data())
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(status=403)
        else:
            user_form = self.form_class(request.POST, request.FILES)
            profile_form = self.profile_form(request.POST, request.FILES)

            if user_form.is_valid() and profile_form.is_valid():
                return self.form_valid(user_form, profile_form)
            else:
                return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        registered = False
        user = user_form.save()
        user.set_password(user.password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.user = user

        if 'profile_pic' in self.request.FILES:
            profile.profile_pic = self.request.FILES['profile_pic']
        profile.save()

        registered = True
        messages.success(self.request, "Registration Successful")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, user_form, profile_form):
        messages.error(self.request, "Correct Errors in the Form")
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = self.form_class(self.request.POST)
            context['profile_form'] = self.profile_form(self.request.POST)
        else:
            context['user_form'] = self.get_form_class()
            context['profile_form'] = self.profile_form()
        return context

    def get_success_url(self):
        return reverse('booking:login')
