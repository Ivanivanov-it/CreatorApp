from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'common/landing_page.html'

    extra_context = {
        'page_title': "Home"
    }

class WipPage(TemplateView):
    template_name = 'common/wip.html'

    extra_context = {
        "page_title": "WIP"
    }

class AboutPageView(TemplateView):
    template_name = 'common/about.html'
    extra_context = {
        'page_title': "About"
    }

class NoPermissionView(TemplateView):
    template_name = 'common/no_permission.html'
    extra_context = {
        'page_title': "No Permission"
    }

class MaintenanceView(TemplateView):
    template_name = 'common/maintenance.html'
    extra_context = {
        'page_title': "Maintenance"
    }

def test_500(request):
    raise Exception('Testing 500 error')

def test_400(request):
    return render(request, "400.html", status=400)