from django.urls import path
from common.views import LandingPageView

app_name = "common"

urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
]