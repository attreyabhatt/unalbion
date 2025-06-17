from django.db import models
from django.contrib.auth.models import User

class PotionInput(models.Model):
    """
    Stores user's market price inputs for ingredients and potion sale prices.
    Calculations are handled on the frontend.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='potion_input'
    )
    updated_at = models.DateTimeField(auto_now=True)

    # === HERBS (T2-T8) ===
    agaric = models.PositiveIntegerField(null=True, blank=True, help_text="Arcane Agaric")
    comfrey = models.PositiveIntegerField(null=True, blank=True, help_text="Brightleaf Comfrey")
    burdock = models.PositiveIntegerField(null=True, blank=True, help_text="Crenellated Burdock")
    teasel = models.PositiveIntegerField(null=True, blank=True, help_text="Dragon Teasel")
    foxglove = models.PositiveIntegerField(null=True, blank=True, help_text="Elusive Foxglove")
    mullein = models.PositiveIntegerField(null=True, blank=True, help_text="Firetouched Mullein")
    yarrow = models.PositiveIntegerField(null=True, blank=True, help_text="Ghoul Yarrow")

    # === ANIMAL PRODUCTS ===
    cow_milk = models.PositiveIntegerField(null=True, blank=True)
    goat_milk = models.PositiveIntegerField(null=True, blank=True)
    sheep_milk = models.PositiveIntegerField(null=True, blank=True)
    
    cow_butter = models.PositiveIntegerField(null=True, blank=True)
    goat_butter = models.PositiveIntegerField(null=True, blank=True)
    sheep_butter = models.PositiveIntegerField(null=True, blank=True)
    
    hen_eggs = models.PositiveIntegerField(null=True, blank=True)
    goose_eggs = models.PositiveIntegerField(null=True, blank=True)

    # === SCHNAPPS ===
    potato_schnapps = models.PositiveIntegerField(null=True, blank=True)
    corn_hooch = models.PositiveIntegerField(null=True, blank=True)
    pumpkin_moonshine = models.PositiveIntegerField(null=True, blank=True)

    # === ENCHANTMENT MATERIALS ===
    animal_remains = models.PositiveIntegerField(null=True, blank=True, help_text="Used for enchanting potions (+1, +2, +3)")



    # === POTION SALE PRICES ===
    # Dynamic field generation for all valid potion combinations
    
    class Meta:
        verbose_name = "Potion Market Data"
        verbose_name_plural = "Potion Market Data"

    def __str__(self):
        return f"{self.user.username}'s Market Data"

    def get_ingredient_price(self, ingredient_code):
        """Get price for an ingredient"""
        return getattr(self, ingredient_code, None)

    def to_dict(self):
        """Convert all prices to a dictionary for JSON serialization"""
        data = {}
        
        # Get all model fields
        for field in self._meta.get_fields():
            if isinstance(field, models.PositiveIntegerField):
                value = getattr(self, field.name)
                if value is not None:
                    data[field.name] = value
        
        return data


# Dynamically add potion sale price fields
def add_potion_price_fields():
    """Add potion sale price fields to the PotionInput model"""
    
    # Valid potion combinations
    POTION_COMBINATIONS = [
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
        ("INVISIBILITY", [8]),  # T8 only
    ]
    
    # Add sale price fields for each potion-tier-enchant combination
    for potion_name, tiers in POTION_COMBINATIONS:
        for tier in tiers:
            for enchant in range(4):  # 0, 1, 2, 3
                field_name = f'T{tier}_{potion_name}_{enchant}'
                
                # Add the field to the model
                field = models.PositiveIntegerField(
                    null=True, 
                    blank=True,
                    help_text=f"Sale price for T{tier} {potion_name.title()} +{enchant}"
                )
                
                # Add to model
                field.contribute_to_class(PotionInput, field_name)

# Execute the dynamic field addition
add_potion_price_fields()