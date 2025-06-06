from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AnimalArtifact, AnimalArtifactItem, ArtifactType

@receiver(post_save, sender=User)
def create_default_artifacts(sender, instance, created, **kwargs):
    if created:
        # Map artifact type to tier prefix
        tier_prefix_map = {
            ArtifactType.RUGGED: 't3',
            ArtifactType.FINE: 't5',
            ArtifactType.EXCELLENT: 't7',
        }

        # Mapping from item display name to short code name
        item_code_map = {
            'Shadow Claws': 'shadow',
            'Sylvian Roots': 'root',
            'Spirit Paws': 'spirit',
            'Werewolf Fangs': 'werewolf',
            "Imp's Horn": 'imp',
            'Runestone Tooth': 'runestone',
            'Dawnfeather': 'dawn',
        }

        # Create one artifact of each type
        for artifact_type, prefix in tier_prefix_map.items():
            artifact = AnimalArtifact.objects.create(user=instance, artifact_type=artifact_type)

            for name, short_code in item_code_map.items():
                AnimalArtifactItem.objects.create(
                    artifact=artifact,
                    name=name,
                    code_name=f"{prefix}{short_code}",
                )
