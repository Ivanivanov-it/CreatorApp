from django.urls import path

from partners.views import partner_detail, create_partner, partners_list, edit_partner, delete_partner

app_name = 'partners'

urlpatterns = [
    path('',partners_list,name='partners_list'),
    path('<int:id>/',partner_detail,name='partner_detail'),
    path('create/',create_partner,name='create_partner'),
    path('edit/<int:id>/',edit_partner,name='edit_partner'),
    path('delete/<int:id>/',delete_partner,name='delete_partner')

]