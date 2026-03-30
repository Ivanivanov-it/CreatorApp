"""
URL configuration for CreatorApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from common.views import WipPage, AboutPageView, NoPermissionView, MaintenanceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('characters/',include('characters.urls')),
    path('enemies/',include('enemies.urls')),
    path('partners/',include('partners.urls')),
    path('contact-us/',include('contacts.urls')),
    path('battle/',include('battle.urls')),
    path('accounts/', include('accounts.urls')),
    path('cards/',include('cards.urls')),
    path('wip/',WipPage.as_view(),name='wip'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('no-permission/',NoPermissionView.as_view(),name='no_permission'),
    path('maintenance/', MaintenanceView.as_view(), name='maintenance'),
    path('api/',include('enemies.api_urls')),
    path('api/',include('characters.api_urls')),
    path('api/',include('partners.api_urls')),
    path('api/',include('accounts.api_urls')),

]