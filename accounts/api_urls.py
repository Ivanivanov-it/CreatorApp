from django.urls import path

from accounts.views import UserStatsListApiView

urlpatterns = [
    path('user_stats/', UserStatsListApiView.as_view(),name='user_stats_api_list'),
]