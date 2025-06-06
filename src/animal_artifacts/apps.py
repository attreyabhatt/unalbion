from django.apps import AppConfig


class AnimalArtifactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animal_artifacts'
    
    def ready(self):
        import animal_artifacts.signals  # make sure signals are loaded
