from django.apps import AppConfig


class UserConfig(AppConfig):
    # 自动递增主键
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
    verbose_name = '用户'
