from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserRegistrationForm, CustomLoginForm, ProfileUpdateForm, CustomUserUpdateForm
from .models import Profile


class RegisterView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        super().form_valid(form)
        messages.success(self.request, f'Account created successfully! Welcome, {self.object.username}!')
        login(self.request, self.object)
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = CustomUserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = CustomUserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, 'Profile updated successfully!')
            return super().form_valid(form)
        else:
            return self.render_to_response(context)