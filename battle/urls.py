from django.urls import path

from battle.views import character_selection, enemy_selection, battle

app_name = 'battle'


urlpatterns = [
    path('character-selection/',character_selection, name='character_selection'),
    path('enemy-selection/',enemy_selection,name="enemy_selection"),
    path('battle/',battle, name='battle'),
]