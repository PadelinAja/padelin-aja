from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        try:
            from django.contrib.auth.models import Group
            Group.objects.get_or_create(name='SiteAdmin')
        except Exception:
            pass
