from django.urls import path

from contacts.views import create_mail, WipPage

app_name = 'contacts'

urlpatterns = [
    path('',create_mail,name='contact-us'),
    path('wip/',WipPage.as_view(),name='wip'),
]