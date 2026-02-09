from django.urls import path, include

from enemies.views import enemy_detail, enemies_list, delete_enemy, create_enemy, edit_enemy

app_name = 'enemies'

urlpatterns = [
    path('', enemies_list, name='enemies_list'),
    path('<int:id>/', include([
        path('', enemy_detail, name='enemy_detail'),
        path('edit/', edit_enemy, name='edit_enemy'),
        path('delete/', delete_enemy, name='delete_enemy'),
    ])),
    path('create/', create_enemy, name='create_enemy')
]
