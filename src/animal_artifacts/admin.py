from django.contrib import admin
from .models import AnimalArtifact, AnimalArtifactItem

class AnimalArtifactItemInline(admin.TabularInline):
    model = AnimalArtifactItem
    extra = 0  # Don't show extra empty rows
    readonly_fields = ('name', 'code_name', 'market_price')  # Optional: Make read-only

@admin.register(AnimalArtifact)
class AnimalArtifactAdmin(admin.ModelAdmin):
    list_display = ('user', 'artifact_type')
    list_filter = ('artifact_type',)
    search_fields = ('user__username',)
    inlines = [AnimalArtifactItemInline]

@admin.register(AnimalArtifactItem)
class AnimalArtifactItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'market_price', 'artifact', 'get_user')
    list_filter = ('name', 'artifact__artifact_type')
    search_fields = ('name', 'code_name', 'artifact__user__username')

    def get_user(self, obj):
        return obj.artifact.user.username
    get_user.short_description = 'User'
