from django.urls import path

from achievements.views import AchievementListView

app_name = 'achievements'


urlpatterns = [
    path("", AchievementListView.as_view(), name='achievements'),
]