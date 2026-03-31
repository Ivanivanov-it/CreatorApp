from accounts.models import UserBattleStats
from battle.choices import BattleAction
from battle.models import Battle, BattleCharacter, BattleEnemy
from common.choices import BattleStatus

HEAL_INTERVAL = 3
BUFF_INTERVAL = 5

class BattleService:

    def __init__(self,battle,character,enemy):
        self.battle: Battle = battle
        self.character: BattleCharacter = character
        self.enemy: BattleEnemy = enemy

    def can_heal(self) -> bool:
        return self.is_player_turn() and self.battle.turns % HEAL_INTERVAL == 0

    def can_buff(self) -> bool:
        return self.is_player_turn() and self.battle.turns % BUFF_INTERVAL == 0

    def process_turn(self,action:str,user) -> None:

        if self.battle.status == BattleStatus.FINISHED:
            return

        if self.is_player_turn():
            self.handle_player_action(action)
        else:
            self.handle_enemy_action()

        self.check_battle_end(user)

        if self.battle.status != BattleStatus.FINISHED:
            self.battle.turns += 1

        self.battle.save()


    def is_player_turn(self) -> bool:
        return self.battle.turns % 2 == 1

    def handle_player_action(self,action:str) -> None:
        if action == BattleAction.HEAL and self.can_heal():
            heal_amount = self.character.total_def
            self.character.heal(heal_amount,battle=self.battle)
        elif action == BattleAction.BUFF and self.can_buff():
            atk_buff_multiplier = 0.5
            def_buff_multiplier = 0.5
            self.character.buff(atk_buff_multiplier,def_buff_multiplier,battle=self.battle)
        else:
            self.enemy.take_damage(self.character.total_atk,battle=self.battle)

    def handle_enemy_action(self) -> None:
        self.character.take_damage(self.enemy.total_atk,battle=self.battle)

    def check_battle_end(self,user) -> None:
        if self.enemy.is_alive and self.character.is_alive:
            return

        stats, _ = UserBattleStats.objects.get_or_create(user=user)
        if self.character.is_alive:
            stats.add_win()
        else:
            stats.add_loss()

        self.battle.status = BattleStatus.FINISHED
        self.battle.save(update_fields=["status"])
