from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from accounts.forms import RegisterForm


# Create your views here.

UserModel = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('characters:home')

    def form_valid(self,form):
        response = super().form_valid(form)
        login(self.request,self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('characters:home')

        return super().dispatch(request, *args, **kwargs)

    extra_context = {
        'page_title': 'Register',
    }


class UserProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/user_profile.html'
    extra_context = {
        'page_title': 'User Profile',
    }


