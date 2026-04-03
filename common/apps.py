from django.apps import AppConfig



class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import create_groups_and_permissions,run_collectstatic,sync_staff_status
        from django.db.models.signals import m2m_changed
        from django.contrib.auth import get_user_model

        User = get_user_model()

        post_migrate.connect(create_groups_and_permissions, sender=self)
        post_migrate.connect(run_collectstatic, sender=self)
        m2m_changed.connect(sync_staff_status, sender=User.groups.through)