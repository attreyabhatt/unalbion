from django.db import models
from django.contrib.auth.models import User

class ArtifactType(models.TextChoices):
    RUGGED = 'Rugged', 'Rugged'
    FINE = 'Fine', 'Fine'
    EXCELLENT = 'Excellent', 'Excellent'

class AnimalArtifact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animal_artifacts')
    artifact_type = models.CharField(max_length=10, choices=ArtifactType.choices)

    def __str__(self):
        return f"{self.user.username}'s {self.artifact_type} Artifact"

class AnimalArtifactItem(models.Model):
    ITEM_CHOICES = [
        ('Shadow Claws', 'Shadow Claws'),
        ('Sylvian Roots', 'Sylvian Roots'),
        ('Spirit Paws', 'Spirit Paws'),
        ('Werewolf Fangs', 'Werewolf Fangs'),
        ("Imp's Horn", "Imp's Horn"),
        ('Runestone Tooth', 'Runestone Tooth'),
        ('Dawnfeather', 'Dawnfeather'),
    ]

    artifact = models.ForeignKey(AnimalArtifact, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100, choices=ITEM_CHOICES)
    market_price = models.PositiveIntegerField(null=True, blank=True)
    code_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code_name}) - ${self.market_price}"
