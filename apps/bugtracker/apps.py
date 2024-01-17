from django.apps import AppConfig


class BugtrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bugtracker'
    verbose_name = '缺陷跟踪'
