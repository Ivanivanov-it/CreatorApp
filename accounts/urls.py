from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserProfileView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('profile/', UserProfileView.as_view(),name='profile'),
]