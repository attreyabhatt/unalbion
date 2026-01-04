from django.db import models
from django.contrib.auth.models import User


class IngredientCategory(models.TextChoices):
    HERB = "HERB", "Herb"
    ANIMAL_PRODUCT = "ANIMAL_PRODUCT", "Animal Product"
    SCHNAPPS = "SCHNAPPS", "Schnapps"
    OTHER = "OTHER", "Other"


class Ingredient(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=IngredientCategory.choices)

    def __str__(self):
        return self.name


class UserIngredientPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ingredient_prices")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="prices")
    price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "ingredient"], name="uniq_user_ingredient"),
        ]
        indexes = [
            models.Index(fields=["user", "ingredient"]),
        ]

    def __str__(self):
        return f"{self.user.username} {self.ingredient.code}: {self.price}"


class PotionVariant(models.Model):
    code = models.CharField(max_length=64, unique=True)
    tier = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    enchant = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.code}"


class UserPotionPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="potion_prices")
    potion = models.ForeignKey(PotionVariant, on_delete=models.CASCADE, related_name="prices")
    price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "potion"], name="uniq_user_potion"),
        ]
        indexes = [
            models.Index(fields=["user", "potion"]),
        ]

    def __str__(self):
        return f"{self.user.username} {self.potion.code}: {self.price}"
