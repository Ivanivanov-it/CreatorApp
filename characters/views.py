from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from characters.forms import CharacterForm, CharacterCreateForm, CharacterEditForm, CharacterSearchForm
from characters.models import Character


# Create your views here.


def landing_page(request: HttpRequest) -> HttpResponse:

    context = {
        'page_title': "Home"
    }

    return render(request,'characters/landing_page.html', context)

def characters_list(request: HttpRequest) -> HttpResponse:
    search_form = CharacterSearchForm(request.GET or None)

    characters = Character.objects.all()

    if 'query' in request.GET:
        if search_form.is_valid():
            characters = characters.filter(Q(name__icontains=search_form.cleaned_data['query']) | Q(title__icontains=search_form.cleaned_data['query']))

    context = {
        'page_title': "Characters",
        'characters': characters,
        'search_form': search_form
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
    form = CharacterCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('characters:characters_list')

    context = {
        'page_title': "Create Character",
        'form': form,
    }

    return render(request,'characters/create_character.html',context)


def edit_character(request: HttpRequest,id: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=id)
    form = CharacterEditForm(request.POST or None,instance=character)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('characters:characters_list')

    context = {
        'page_title': "Edit Character",
        'form': form,
    }

    return render(request, 'characters/edit_character.html', context)


def delete_character(request: HttpRequest,id: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=id)

    if character:
        character.delete()

    return redirect('characters:characters_list')