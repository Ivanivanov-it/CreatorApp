from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from accounts.models import UserBattleStats
from battle.models import Battle, BattleCharacter, BattleEnemy, BattleLog
from battle.services import BattleService
from battle.stat_calc_functions import calc_buff_atk, calc_buff_def, calc_buff_hp, calc_debuff_atk, calc_debuff_hp, \
    calc_debuff_def
from characters.forms import CharacterSearchForm
from characters.models import Character
from common.choices import BattleStatus
from enemies.forms import EnemySearchForm
from enemies.models import Enemy
from partners.models import Partner


class CharacterSelectionView(LoginRequiredMixin,ListView):
    model = Character
    template_name = "battle/select_character.html"
    context_object_name = 'characters'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('card_theme')
        self.search_form = CharacterSearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']

            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Character Selection"

        return context

    def post(self,request,*args,**kwargs):
        character_id = request.POST.get("character_id")
        request.session["character_id"] = character_id

        return redirect("battle:partner_selection")


class PartnerSelectionView(LoginRequiredMixin,ListView):
    template_name = "battle/select_partner.html"
    context_object_name = 'partners'
    paginate_by = 9
    ordering = ['name']

    def dispatch(self,request,*args,**kwargs):
        if not request.session.get("character_id"):
            return redirect("battle:character_selection")
        return super().dispatch(request,*args,**kwargs)

    def get_queryset(self):
        return Partner.objects.filter(character=self.request.session["character_id"]).select_related('card_theme').order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Partner Selection"
        return context

    def post(self,request,*args,**kwargs):
        partner_id = request.POST.get("partner_id")
        request.session["partner_id"] = partner_id
        return redirect("battle:enemy_selection")

class EnemySelectionView(LoginRequiredMixin,ListView):
    model = Enemy
    template_name = "battle/select_enemy.html"
    context_object_name = 'enemies'
    paginate_by = 9
    ordering = ['name']

    def dispatch(self,request,*args,**kwargs):
        if not request.session.get("character_id"):
            return redirect("battle:character_selection")
        return super().dispatch(request,*args,**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().select_related('card_theme')
        self.search_form = EnemySearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']

            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Enemy Selection"
        return context

    def post(self,request,*args,**kwargs):
        enemy_id = request.POST.get("enemy_id")
        request.session["enemy_id"] = enemy_id
        return redirect("battle:create_battle")


class CreateBattleView(LoginRequiredMixin,View):

    def dispatch(self, request, *args, **kwargs):
        character_id = request.session.get("character_id")
        enemy_id = request.session.get("enemy_id")

        if not character_id or not enemy_id:
            return redirect("battle:character_selection")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        character_id = request.session.get("character_id")
        partner_id = request.session.get("partner_id", [])
        enemy_id = request.session.get("enemy_id")

        character = Character.objects.get(id=character_id)
        enemy = Enemy.objects.get(id=enemy_id)
        partner = Partner.objects.get(id=partner_id) if partner_id else None

        battle = Battle.objects.create(creator=request.user)

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
            debuff_hp=calc_debuff_hp(enemy, character),
            debuff_atk=calc_debuff_atk(enemy, character),
            debuff_def=calc_debuff_def(enemy, character)
        )

        return redirect("battle:battle_view", pk=battle.id)


class BattleView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    template_name = "battle/battle.html"
    model = Battle

    def test_func(self):
        battle = self.get_object()
        return (
            self.request.user == battle.creator or
            self.request.user.groups.filter(name="BattleManager").exists()
        )

    def handle_no_permission(self):

        return redirect('no_permission')

    def get_combatants(self,battle):
        character = battle.battlecharacter_set.select_related("character__card_theme").first()
        enemy = battle.battleenemy_set.select_related("enemy__card_theme").first()
        return character, enemy

    def build_context(self,battle,character,enemy):
        return {
            "battle": battle,
            "character": character,
            "enemy": enemy,
            "logs": BattleLog.objects.filter(battle=battle),
            "can_heal": BattleService(battle,character,enemy).can_heal(),
            "can_buff": BattleService(battle,character,enemy).can_buff(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        character,enemy= self.get_combatants(self.object)
        context.update(self.build_context(self.object,character,enemy))

        return context

    def post(self,request,*args,**kwargs):
        battle = self.get_object()
        character,enemy = self.get_combatants(battle)
        action = request.POST.get("action","attack")

        BattleService(battle,character,enemy).process_turn(action,request.user)


        return render(request, self.template_name, context=self.build_context(battle,character,enemy))


async def leaderboard_api(request):
    get_stats = sync_to_async(
        lambda: list(
            UserBattleStats.objects.select_related('user')
            .order_by('-wins','losses')[:10]
        )
    )

    stats = await get_stats()

    data = [
        {
            'username': stat.user.username,
            'wins': stat.wins,
            'losses': stat.losses,
            'winrate': stat.get_user_winrate()
        }
        for stat in stats
    ]

    return JsonResponse({'leaderboard': data})

class LeaderboardView(LoginRequiredMixin,TemplateView):
    template_name = "battle/leaderboard.html"
    extra_context = {
        'page_title': 'Leaderboard',
    }





