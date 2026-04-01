from django.urls import path

from common import views
from common.views import LandingPageView

app_name = "common"

urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
    path('test-400/', views.test_400, name='test-400'),
    path('test-500/', views.test_500, name='test-500'),
]