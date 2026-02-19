from django.urls import path

from battle.views import character_selection, enemy_selection, partner_selection, create_battle, battle_view

app_name = 'battle'


urlpatterns = [
    path('character-selection/',character_selection, name='character_selection'),
    path('partner-selection/',partner_selection, name='partner_selection'),
    path('enemy-selection/',enemy_selection,name="enemy_selection"),
    path('create-battle/',create_battle, name='create_battle'),
    path('<int:pk>/',battle_view,name="battle_view")
]