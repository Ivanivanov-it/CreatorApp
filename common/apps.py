from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import create_groups_and_permissions
        post_migrate.connect(create_groups_and_permissions, sender=self)