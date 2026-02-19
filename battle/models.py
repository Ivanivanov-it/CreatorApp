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

    buff_hp = models.IntegerField(blank=True,default=0)
    buff_atk = models.IntegerField(blank=True,default=0)
    buff_def = models.IntegerField(blank=True,default=0)

    debuff_hp = models.IntegerField(blank=True,default=0)
    debuff_atk = models.IntegerField(blank=True,default=0)
    debuff_def = models.IntegerField(blank=True,default=0)

    current_hp = models.IntegerField(blank=True)
    current_atk = models.IntegerField(blank=True)
    current_def = models.IntegerField(blank=True)
    is_alive = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        self.current_hp = self.base_hp + self.buff_hp - self.debuff_hp
        self.current_atk = self.base_atk + self.buff_atk - self.debuff_atk
        self.current_def = self.base_def + self.buff_def - self.debuff_def

        super().save(*args, **kwargs)


    class Meta:
        abstract = True


class BattleCharacter(BattleParticipant):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)



class BattleEnemy(BattleParticipant):
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)





