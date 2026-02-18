from django.urls import path

from contacts.views import create_mail, WipPage, AboutPageView

app_name = 'contacts'

urlpatterns = [
    path('',create_mail,name='contact-us'),
    path('wip/',WipPage.as_view(),name='wip'),
    path('about/',AboutPageView.as_view(),name='about')
]