from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from accounts.views import RegisterView, UserProfileView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='accounts/password-change.html',
        success_url=reverse_lazy('account:password_change_done')),
        name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/password-change-done.html'),name='password_change_done'),
]