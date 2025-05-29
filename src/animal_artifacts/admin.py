from django.contrib import admin

# Register your models here.
from .models import AnimalArtifact, AnimalArtifactItem
@admin.register(AnimalArtifact)
class AnimalArtifactAdmin(admin.ModelAdmin):
    list_display = ('tier',)
    search_fields = ('tier',)
@admin.register(AnimalArtifactItem)
class AnimalArtifactItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'artifact_tier', 'market_price')
    search_fields = ('name',)
    list_filter = ('artifact_tier',)
    ordering = ('name',)
