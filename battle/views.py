
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from characters.models import Character


# Create your views here.


def character_selection(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        character_id = request.POST.get("character_id")


        request.session["character_id"] = character_id

        return redirect("battle:enemy_selection")

    characters = Character.objects.all()

    context = {
        'characters': characters,
         'page_title': "Character Selection"
    }

    return render(request,"battle/select_character.html",context=context)


def enemy_selection(request: HttpRequest) -> HttpResponse:
    pass

def battle(request: HttpRequest) -> HttpResponse:
    pass
