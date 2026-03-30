from django.urls import path

from contacts.views import CreateMailView, ContactsListView, \
    FinishView

app_name = 'contacts'

urlpatterns = [
    path('',CreateMailView.as_view(),name='contact-us'),
    path('user-contacts/', ContactsListView.as_view(), name='user-contacts'),
    path('<int:pk>/finish/', FinishView.as_view(), name='finish'),
]