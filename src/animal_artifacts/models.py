from django.db import models



class AnimalArtifact(models.Model):
    animal_artifact_tiers = [
    ('Rugged', 'Rugged'),
    ('Fine', 'Fine'),
    ('Excellent', 'Excellent'),
    ]

    tier = models.CharField(max_length=100, unique=True,choices=animal_artifact_tiers)

    def __str__(self):
        return self.tier

class AnimalArtifactItem(models.Model):
    artifact_tier = models.ForeignKey(AnimalArtifact, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    market_price = models.PositiveIntegerField(null=True, blank=True)
    code_name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name