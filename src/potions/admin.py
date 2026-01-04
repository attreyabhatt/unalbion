from django.contrib import admin
from .models import Ingredient, UserIngredientPrice, PotionVariant, UserPotionPrice


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category")
    search_fields = ("code", "name")
    list_filter = ("category",)


@admin.register(UserIngredientPrice)
class UserIngredientPriceAdmin(admin.ModelAdmin):
    list_display = ("user", "ingredient", "price")
    search_fields = ("user__username", "ingredient__code")
    list_filter = ("ingredient__category",)


@admin.register(PotionVariant)
class PotionVariantAdmin(admin.ModelAdmin):
    list_display = ("code", "tier", "name", "enchant")
    search_fields = ("code", "name")
    list_filter = ("tier", "name", "enchant")


@admin.register(UserPotionPrice)
class UserPotionPriceAdmin(admin.ModelAdmin):
    list_display = ("user", "potion", "price")
    search_fields = ("user__username", "potion__code")
    list_filter = ("potion__tier", "potion__name", "potion__enchant")
