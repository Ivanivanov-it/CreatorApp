from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def landing_page(request: HttpRequest) -> HttpResponse:

    context = {
        'page_title': "Home"
    }

    return render(request,'characters/landing_page.html', context)

def characters_list(request: HttpRequest) -> HttpResponse:
    pass

def character_detail(request: HttpRequest,id: int) -> HttpResponse:
    pass

def create_character(request: HttpRequest) -> HttpResponse:
    pass

def edit_character(request: HttpRequest,id: int) -> HttpResponse:
    pass

def delete_character(request: HttpRequest,id: int) -> HttpResponse:
    pass