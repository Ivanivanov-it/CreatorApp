from django.urls import path, include

from enemies.views import enemy_detail, enemies_list, create_enemy, edit_enemy, EnemyDeleteView

app_name = 'enemies'

urlpatterns = [
    path('', enemies_list, name='enemies_list'),
    path('<int:pk>/', include([
        path('', enemy_detail, name='enemy_detail'),
        path('edit/', edit_enemy, name='edit_enemy'),
        path('delete/', EnemyDeleteView.as_view(), name='delete_enemy'),
    ])),
    path('create/', create_enemy, name='create_enemy')
]
