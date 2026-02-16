from django.urls import path

from contacts.views import create_mail

app_name = 'contacts'

urlpatterns = [
    path('',create_mail,name='contact-us'),
]