


def create_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
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


def run_collectstatic(sender,**kwargs):
    from django.core.management import call_command
    call_command('collectstatic', '--noinput',verbosity=0)

def sync_staff_status(sender, instance, action, pk_set, **kwargs):
    from django.contrib.auth.models import Group

    STAFF_GROUPS = {'Moderators', 'BattleManager', 'ContactManagers'}

    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    staff_groups = Group.objects.filter(name__in=STAFF_GROUPS)
    staff_group_ids = set(staff_groups.values_list('id', flat=True))


    user_groups = set(instance.groups.values_list('id', flat=True))
    should_be_staff = bool(user_groups & staff_group_ids)
    if instance.is_staff != should_be_staff:
        instance.is_staff = should_be_staff
        instance.save(update_fields=['is_staff'])