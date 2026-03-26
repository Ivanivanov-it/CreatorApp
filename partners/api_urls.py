from django.urls import path


from partners.views import PartnerListApiView

urlpatterns = [
    path('partners/', PartnerListApiView.as_view(),name='partners_api_list'),
]