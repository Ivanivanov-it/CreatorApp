from django.urls import path

from cards.views import CardListView, CardCreateView

app_name = "cards"

urlpatterns = [
    path('',CardListView.as_view(), name='cards_list'),
    path('create/',CardCreateView.as_view(), name='cards_create'),
]