from django.apps import AppConfig


class SchoolAppConfig(AppConfig):
    name = 'school'

    def ready(self):
        from .signals import create_profile, save_profile