from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from achievements.achievement_tracker import check_and_award_battle_achievements
from cards.models import Card
from characters.models import Character
from enemies.models import Enemy
from partners.models import Partner


def award(user,instance):
    newly_earned = async_to_sync(check_and_award_battle_achievements)(user)
    instance.newly_earned = newly_earned

@receiver(post_save,sender=Character)
def on_character_created(sender,instance,created,**kwargs):
    if created:
        award(instance.creator,instance)

@receiver(post_save, sender=Enemy)
def on_enemy_created(sender, instance, created, **kwargs):
    if created:
        award(instance.creator,instance)


@receiver(post_save, sender=Card)
def on_card_created(sender, instance, created, **kwargs):
    if created:
        award(instance.creator,instance)


@receiver(post_save, sender=Partner)
def on_partner_created(sender, instance, created, **kwargs):
    if created:
        award(instance.creator,instance)