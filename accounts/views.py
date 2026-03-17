from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm


# Create your views here.

class RegisterView(View):

    def get(self, request):
        form = RegisterForm()

        context = {
            'form': form,
            'page_title': 'Register',
        }

        return render(request, 'accounts/register.html', context=context)

    def post(self, request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('characters:home')

        context = {
            'form': form,
            'page_title': 'Register',
        }

        return render(request, 'accounts/register.html', context=context)





