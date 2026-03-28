from django.conf import settings
from django.db import models

from cards.choices import BorderStyleChoices
from characters.models import Character
from common.models import TimeStampModel
from enemies.models import Enemy
from partners.models import Partner


# Create your models here.



class Card(TimeStampModel):
    name = models.CharField(max_length=100)
    border_color = models.CharField(max_length=7)
    border_style = models.CharField(
        max_length=50,
        choices=BorderStyleChoices.choices,
        default=BorderStyleChoices.SOLID
    )
    background_color = models.CharField(max_length=7)
    image_border_color = models.CharField(max_length=7)
    image_border_style = models.CharField(
        max_length=50,
        choices=BorderStyleChoices.choices,
        default=BorderStyleChoices.SOLID
    )
    accent_color = models.CharField(max_length=7)
    is_default = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)

class CharacterCardTheme(TimeStampModel):
    character = models.ForeignKey(Character,on_delete=models.CASCADE,related_name='card_theme')
    theme = models.ForeignKey(Card,on_delete=models.SET_NULL,null=True,blank=True)

class PartnerCardTheme(TimeStampModel):
    partner = models.ForeignKey(Partner,on_delete=models.CASCADE,related_name='card_theme')
    theme = models.ForeignKey(Card,on_delete=models.SET_NULL,null=True,blank=True)

class EnemyCardTheme(TimeStampModel):
    enemy = models.ForeignKey(Enemy,on_delete=models.CASCADE,related_name='card_theme')
    theme = models.ForeignKey(Card,on_delete=models.SET_NULL,null=True,blank=True)

