from django.apps import AppConfig


class ProblemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'problems'
    verbose_name = 'Desafios de Programação'
    
    def ready(self):
        import problems.signals

