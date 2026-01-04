from django.db import models
from django.contrib.auth.models import User


class ArtifactTier(models.TextChoices):
    RUGGED = "RUGGED", "Rugged (T3)"
    FINE = "FINE", "Fine (T5)"
    EXCELLENT = "EXCELLENT", "Excellent (T7)"


ARTIFACT_TIER_PREFIX = {
    ArtifactTier.RUGGED: "t3",
    ArtifactTier.FINE: "t5",
    ArtifactTier.EXCELLENT: "t7",
}

ARTIFACT_TIER_NUMBER = {
    ArtifactTier.RUGGED: 3,
    ArtifactTier.FINE: 5,
    ArtifactTier.EXCELLENT: 7,
}


class ArtifactItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code_base = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ArtifactPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="artifact_prices")
    item = models.ForeignKey(ArtifactItem, on_delete=models.CASCADE, related_name="prices")
    tier = models.CharField(max_length=10, choices=ArtifactTier.choices)
    price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "item", "tier"], name="uniq_user_item_tier"),
        ]
        indexes = [
            models.Index(fields=["user", "item"]),
        ]

    def code_name(self):
        return f"{ARTIFACT_TIER_PREFIX[self.tier]}{self.item.code_base}"

    def __str__(self):
        return f"{self.user.username} {self.item.name} {self.tier}: {self.price}"


ARTIFACT_ITEMS = [
    ("Shadow Claws", "shadow"),
    ("Sylvian Roots", "root"),
    ("Spirit Paws", "spirit"),
    ("Werewolf Fangs", "werewolf"),
    ("Imp's Horn", "imp"),
    ("Runestone Tooth", "runestone"),
    ("Dawnfeather", "dawn"),
]


def ensure_artifact_catalog():
    existing = set(ArtifactItem.objects.values_list("code_base", flat=True))
    missing = [
        ArtifactItem(name=name, code_base=code_base)
        for name, code_base in ARTIFACT_ITEMS
        if code_base not in existing
    ]
    if missing:
        ArtifactItem.objects.bulk_create(missing)
