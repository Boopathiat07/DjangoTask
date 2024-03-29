from django.apps import AppConfig
from django.conf import settings

class OperationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operation'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import operator
            operator.start()

