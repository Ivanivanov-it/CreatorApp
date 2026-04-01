from django.db.models.signals import post_migrate
from django.dispatch import receiver

# common/signals.py
def create_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from django.apps import apps as django_apps

    from django.contrib.auth.management import create_permissions
    for app_config in django_apps.get_app_configs():
        create_permissions(app_config, verbosity=0)


    moderators, _ = Group.objects.get_or_create(name='Moderators')
    moderators_permissions = Permission.objects.filter(codename__in=[
        'add_character', 'change_character', 'delete_character', 'view_character',
        'add_partner',   'change_partner',   'delete_partner',   'view_partner',
        'add_enemy',     'change_enemy',     'delete_enemy',     'view_enemy',
        'add_card',      'change_card',      'delete_card',      'view_card',
    ])
    moderators.permissions.set(moderators_permissions)


    battle_manager, _ = Group.objects.get_or_create(name='BattleManager')
    battle_manager_permissions = Permission.objects.filter(codename__in=[
        'add_battle',    'change_battle',    'delete_battle',    'view_battle',
        'add_battlelog', 'change_battlelog', 'delete_battlelog', 'view_battlelog',
    ])
    battle_manager.permissions.set(battle_manager_permissions)


    contact_manager, _ = Group.objects.get_or_create(name='ContactManagers')
    contact_manager_permissions = Permission.objects.filter(codename__in=[
        'add_contact', 'change_contact', 'delete_contact', 'view_contact',
    ])
    contact_manager.permissions.set(contact_manager_permissions)