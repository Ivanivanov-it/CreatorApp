from django.urls import path

from battle.views import leaderboard_api

urlpatterns = [
    path('leaderboard/', leaderboard_api, name='leaderboard_api'),

]