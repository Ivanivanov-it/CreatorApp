from django.urls import path, include

from characters.views import characters_list, character_detail, create_character, \
    edit_character, LandingPageView, CharacterDeleteView, AboutPageView

app_name = 'characters'

urlpatterns = [
    path('',LandingPageView.as_view(),name='home'),
    path('characters/',include([
        path('',characters_list,name='characters_list'),
        path('about/',AboutPageView.as_view(),name='about'),
        path('<int:pk>/', include ([
            path('',character_detail,name='character_detail'),
        path('edit/',edit_character,name='edit_character'),
        path('delete/',CharacterDeleteView.as_view(),name='delete_character')
        ])),
        path('create/',create_character,name='create_character')
    ]))
]