from django.urls import path

from reviews.views import reviews_list, review_detail, create_review, edit_review, delete_review, like_review

app_name = 'reviews'

urlpatterns = [
    path('',reviews_list,name='reviews_list'),
    path('<int:id>/',review_detail,name='review_detail'),
    path('create/',create_review,name='create_review'),
    path('edit/<int:id>/',edit_review,name='edit_review'),
    path('delete/<int:id>/',delete_review,name='delete_review'),
    path('like/<int:id>/',like_review,name='like_review'),
]