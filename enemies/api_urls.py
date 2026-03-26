from django.urls import path

from enemies.views import EnemyListApiView

urlpatterns = [
    path('enemies/', EnemyListApiView.as_view(),name='enemies_api_list'),
]