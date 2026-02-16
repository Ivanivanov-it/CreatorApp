from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView
from django.views.generic import TemplateView

from characters.forms import CharacterForm, CharacterCreateForm, CharacterEditForm, CharacterSearchForm
from characters.models import Character


# Create your views here.




class LandingPageView(TemplateView):
    template_name = 'characters/landing_page.html'

    extra_context = {
        'page_title': "Home"
    }



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



def character_detail(request: HttpRequest,pk: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=pk)
    context = {
        'page_title': f"{character.name} Details",
        'character': character,
    }

    return render(request,'characters/character_page.html',context)

# class CharacterListView(ListView):
#     model = Character
#     template_name = 'characters/character_page.html'
#     extra_context = {
#         'page_title': "Character details",
#     }

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


def edit_character(request: HttpRequest,pk: int) -> HttpResponse:
    character = get_object_or_404(Character, pk=pk)
    form = CharacterEditForm(request.POST or None,instance=character)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('characters:characters_list')

    context = {
        'page_title': "Edit Character",
        'form': form,
    }

    return render(request, 'characters/edit_character.html', context)


class CharacterDeleteView(DeleteView):
    model = Character
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('characters:characters_list')
