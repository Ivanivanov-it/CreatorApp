
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from battle.models import Battle, BattleCharacter, BattleEnemy
from battle.stat_calc_functions import calc_buff_atk, calc_buff_def, calc_buff_hp, calc_debuff_atk, calc_debuff_hp, \
    calc_debuff_def
from characters.models import Character
from common.choices import BattleStatus
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
    enemy = Enemy.objects.get(id=enemy_id)

    if partner_id:
        partner = Partner.objects.get(id=partner_id)

    BattleCharacter.objects.create(
        battle=battle,
        character=character,
        base_hp=character.hp,
        base_atk=character.attack,
        base_def=character.defense,
        buff_hp=calc_buff_hp(character) + (partner.hp if partner_id else 0),
        buff_atk=calc_buff_atk(character) + (partner.attack if partner_id else 0),
        buff_def=calc_buff_def(character) + (partner.defense if partner_id else 0),
    )

    BattleEnemy.objects.create(
        battle=battle,
        enemy=enemy,
        base_hp=enemy.hp,
        base_atk=enemy.attack,
        base_def=enemy.defense,
        buff_hp=calc_buff_hp(enemy),
        buff_atk=calc_buff_atk(enemy),
        buff_def=calc_buff_def(enemy),
        debuff_hp=calc_debuff_hp(enemy,character),
        debuff_atk=calc_debuff_atk(enemy,character),
        debuff_def=calc_debuff_def(enemy,character)
    )

    return redirect("battle:battle_view",pk=battle.id)

def battle_view(request: HttpRequest,pk:int) -> HttpResponse:
    battle = get_object_or_404(Battle,pk=pk)

    if not battle:
        return redirect("battle:character_selection")

    character = battle.battlecharacter_set.first()
    enemy = battle.battleenemy_set.first()

    if request.method == "POST":
        battle = get_object_or_404(Battle,pk=pk)
        character = battle.battlecharacter_set.first()
        enemy = battle.battleenemy_set.first()

        turn = battle.turns



        if turn % 2 == 1:
            enemy.take_damage(character.total_atk)
        else:
            character.take_damage(enemy.total_atk)

        if not enemy.is_alive or not character.is_alive:
            battle.status = BattleStatus.finished

        turn += 1

        battle.turns = turn
        battle.save()


        context = {
            "battle": battle,
            "character": character,
            "enemy": enemy
        }


        return render(request, "battle/battle.html", context=context)


    context = {
        "battle": battle,
        "character": character,
        "enemy": enemy,
    }

    return render(request,"battle/battle.html",context=context)




