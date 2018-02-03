from django.apps import AppConfig
from django.db.models.signals import post_save

class DoubanConfig(AppConfig):
    name = 'douban'

    def ready(self):
        from .signals import django_trigger 
