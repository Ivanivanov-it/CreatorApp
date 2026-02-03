from django.urls import path, include

from reviews.views import reviews_list, review_detail, create_review, edit_review, delete_review, like_review

app_name = 'reviews'

urlpatterns = [
    path('',reviews_list,name='reviews_list'),
    path('<int:id>', include ([
        path('',review_detail,name='review_detail'),
        path('edit/',edit_review,name='edit_review'),
    path('delete/',delete_review,name='delete_review'),
    path('like/',like_review,name='like_review')
    ])),
    path('create/',create_review,name='create_review'),
]