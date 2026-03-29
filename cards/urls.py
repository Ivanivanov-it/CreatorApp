from django.urls import path

from cards.views import CardListView, CardCreateView, CardDetailView, EditCardView, CardDeleteView

app_name = "cards"

urlpatterns = [
    path('',CardListView.as_view(), name='cards_list'),
    path('create/',CardCreateView.as_view(), name='cards_create'),
    path('<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('<int:pk>/edit/', EditCardView.as_view(),name='edit_card'),
    path('<int:pk>/delete/', CardDeleteView.as_view(),name='card_delete'),
]