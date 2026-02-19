from django.db import models

from characters.models import Character
from common.choices import BattleStatus
from common.models import TimeStampModel
from enemies.models import Enemy


# Create your models here.

class Battle(TimeStampModel):

    status = models.CharField(max_length=20,choices=BattleStatus.choices,default=BattleStatus.active)
    turns = models.IntegerField(default=1)


class BattleParticipant(TimeStampModel):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)

    base_hp = models.IntegerField()
    base_atk = models.IntegerField()
    base_def = models.IntegerField()

    current_hp = models.IntegerField()
    current_atk = models.IntegerField()
    current_def = models.IntegerField()

    is_alive = models.BooleanField(default=True)

    class Meta:
        abstract = True


class BattleCharacter(BattleParticipant):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)



class BattleEnemy(BattleParticipant):
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)

