from django.urls import path

from characters.views import CharacterListApiView

urlpatterns = [
    path('characters/', CharacterListApiView.as_view(),name='characters_api_list'),
]