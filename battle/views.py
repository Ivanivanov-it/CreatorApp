
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from battle.models import Battle, BattleCharacter
from battle.stat_calc_functions import calc_buff_atk, calc_buff_def, calc_buff_hp
from characters.models import Character
from enemies.models import Enemy
from partners.models import Partner





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

        return redirect("battle:create_battle")

    enemies = Enemy.objects.all()

    context = {
        'enemies': enemies,
         'page_title': "Enemy Selection"
    }

    return render(request,"battle/select_enemy.html",context=context)

def create_battle(request: HttpRequest) -> HttpResponse:
    character_id = request.session.get("character_id")
    partner_id = request.session.get("partner_id",[])
    enemy_id = request.session.get("enemy_id")

    if not character_id or not enemy_id:
        return redirect("battle:character_selection")

    battle = Battle.objects.create()

    character = Character.objects.get(id=character_id)

    if partner_id:
        partner = Partner.objects.get(id=partner_id)

    BattleCharacter.objects.create(
        battle=battle,
        character=character,
        base_hp=character.hp,
        base_atk=character.attack,
        base_def=character.defense,
        buff_hp=calc_buff_hp(character) + partner.hp if partner_id else 0,
        buff_atk=calc_buff_atk(character) + partner.attack if partner_id else 0,
        buff_def=calc_buff_def(character) + partner.defense if partner_id else 0,

    )





