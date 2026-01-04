from django.contrib import admin
from .models import ArtifactItem, ArtifactPrice, ArtifactTier


@admin.register(ArtifactItem)
class ArtifactItemAdmin(admin.ModelAdmin):
    list_display = ("name", "code_base")
    search_fields = ("name", "code_base")


@admin.register(ArtifactPrice)
class ArtifactPriceAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "tier", "price")
    search_fields = ("user__username", "item__name", "item__code_base")
    list_filter = ("tier",)
