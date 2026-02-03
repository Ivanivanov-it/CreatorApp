from django.urls import path, include

from partners.views import partners_list, partner_detail, create_partner, edit_partner, delete_partner

app_name = 'partners'

urlpatterns = [
    path('', partners_list, name='partners_list'),
    path('<int:id>/', include([
        path('', partner_detail, name='partner_detail'),
        path('edit/', edit_partner, name='edit_partner'),
        path('delete/', delete_partner, name='delete_partner'),
    ])),
    path('create/', create_partner, name='create_partner')
]
