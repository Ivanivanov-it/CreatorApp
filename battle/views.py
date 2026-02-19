
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from characters.models import Character
from enemies.models import Enemy
from partners.models import Partner


# Create your views here.


def character_selection(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        character_id = request.POST.get("character_id")


        request.session["character_id"] = character_id

        print(character_id)

        return redirect("battle:partner_selection")

    characters = Character.objects.all()

    context = {
        'characters': characters,
         'page_title': "Character Selection"
    }

    return render(request,"battle/select_character.html",context=context)

def partner_selection(request: HttpRequest) -> HttpResponse:

    character_id = request.session.get("character_id")

    if not character_id:
        return redirect("battle:character_selection")

    partners = Partner.objects.filter(character_id=character_id)

    if request.method == "POST":
        partner_id = request.POST.get("partner_id")


        request.session["partner_id"] = partner_id

        return redirect("battle:enemy_selection")


    context = {
        'partners': partners,
         'page_title': "Partner Selection"
    }

    return render(request,"battle/select_partner.html",context=context)


def enemy_selection(request: HttpRequest) -> HttpResponse:

    character_id = request.session.get("character_id")

    if not character_id:
        return redirect("battle:character_selection")



    if request.method == "POST":
        enemy_id = request.POST.get("enemy_id")


        request.session["enemy_id"] = enemy_id

        return redirect("battle:battle")

    enemies = Enemy.objects.all()

    context = {
        'enemies': enemies,
         'page_title': "Enemy Selection"
    }

    return render(request,"battle/select_enemy.html",context=context)

def battle(request: HttpRequest) -> HttpResponse:
    pass
