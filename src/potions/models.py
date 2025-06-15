# potions/models.py
from django.db import models
from django.contrib.auth.models import User

class PotionInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='potion_inputs')
    created_at = models.DateTimeField(auto_now_add=True)

    # Herb prices (internal names, full names will be shown in the frontend)
    agaric = models.PositiveIntegerField(null=True, blank=True)       # Arcane Agaric Seed (T2)
    comfrey = models.PositiveIntegerField(null=True, blank=True)      # Brightleaf Comfrey Seed (T3)
    burdock = models.PositiveIntegerField(null=True, blank=True)      # Crenellated Burdock Seed (T4)
    teasel = models.PositiveIntegerField(null=True, blank=True)       # Dragon Teasel Seed (T5)
    foxglove = models.PositiveIntegerField(null=True, blank=True)     # Elusive Foxglove Seed (T6)
    mullein = models.PositiveIntegerField(null=True, blank=True)      # Firetouched Mullein Seed (T7)
    yarrow = models.PositiveIntegerField(null=True, blank=True)       # Ghoul Yarrow Seed (T8)

    # Animal products (specific subtypes)
    cow_milk = models.PositiveIntegerField(null=True, blank=True)
    goat_milk = models.PositiveIntegerField(null=True, blank=True)
    sheep_milk = models.PositiveIntegerField(null=True, blank=True)

    cow_butter = models.PositiveIntegerField(null=True, blank=True)
    goat_butter = models.PositiveIntegerField(null=True, blank=True)
    sheep_butter = models.PositiveIntegerField(null=True, blank=True)

    hen_eggs = models.PositiveIntegerField(null=True, blank=True)
    goose_eggs = models.PositiveIntegerField(null=True, blank=True)

    # Schnapps (specific subtypes)
    potato_schnapps = models.PositiveIntegerField(null=True, blank=True)
    corn_hooch = models.PositiveIntegerField(null=True, blank=True)
    pumpkin_moonshine = models.PositiveIntegerField(null=True, blank=True)

    animal_remains = models.PositiveIntegerField(null=True, blank=True)

    # Valid potion-tier-enchant combinations
    # Format: T{tier}_{NAME}_{enchant}
    for potion, tiers in [
        ("ENERGY", [2, 4, 6]),
        ("HEALING", [2, 4, 6]),
        ("GIGANTIFY", [3, 5, 7]),
        ("RESISTANCE", [3, 5, 7]),
        ("ACID", [3, 5, 7]),
        ("CALMING", [3, 5, 7]),
        ("CLEANSING", [3, 5, 7]),
        ("STICKY", [3, 5, 7]),
        ("POISON", [4, 6, 8]),
        ("GATHERING", [4, 6, 8]),
        ("HELLFIRE", [4, 6, 8]),
        ("BERSERK", [4, 6, 8]),
        ("TORNADO", [4, 6, 8]),
    ]:
        for tier in tiers:
            for enchant in range(4):
                field_name = f'T{tier}_{potion}_{enchant}'
                locals()[field_name] = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PotionInput by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
