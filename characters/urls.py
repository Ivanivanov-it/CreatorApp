from django.urls import path, include

from characters.views import landing_page, characters_list, character_detail, create_character, delete_character, \
    edit_character

app_name = 'characters'

urlpatterns = [
    path('',landing_page,name='home'),
    path('characters/',include([
        path('',characters_list,name='characters_list'),
        path('<int:id>/', include ([
            path('',character_detail,name='character_detail'),
        path('edit/',edit_character,name='edit_character'),
        path('delete/',delete_character,name='delete_character')
        ])),
        path('create/',create_character,name='create_character')
    ]))
]