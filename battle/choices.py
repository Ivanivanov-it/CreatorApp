from django.db import models


class BattleAction(models.TextChoices):
    ATTACK = 'attack', 'Attack'
    HEAL = 'heal', 'Heal'
    BUFF = 'buff', 'Buff'