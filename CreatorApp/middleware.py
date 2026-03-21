from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


class MaintenanceMiddleware:
    """Maintenance Middleware that I will probably never use but I wanted to add 1 to the project."""


    EXEMPT_URLS = [
        '/contact-us/maintenance/',
        '/static/',
        '/media/',
        '/admin/',
        '/admin',
        '/accounts/login/'
    ]

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE', False):
            is_exempt = any(request.path.startswith(url) for url in self.EXEMPT_URLS)

            if not is_exempt and not request.user.is_staff:
                return redirect('contacts:maintenance')

        return self.get_response(request)