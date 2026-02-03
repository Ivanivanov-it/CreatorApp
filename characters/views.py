from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from characters.models import Character


# Create your views here.


def landing_page(request: HttpRequest) -> HttpResponse:

    context = {
        'page_title': "Home"
    }

    return render(request,'characters/landing_page.html', context)

def characters_list(request: HttpRequest) -> HttpResponse:
    characters = Character.objects.all()

    context = {
        'page_title': "Characters",
        'characters': characters,
    }

    return render(request,'characters/characters_page.html',context)

def character_detail(request: HttpRequest,id: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=id)
    context = {
        'page_title': f"{character.name} Details",
        'character': character,
    }

    return render(request,'characters/character_page.html',context)

def create_character(request: HttpRequest) -> HttpResponse:
    pass

def edit_character(request: HttpRequest,id: int) -> HttpResponse:
    pass

def delete_character(request: HttpRequest,id: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=id)

    if character:
        character.delete()

    return redirect('characters:characters_list')