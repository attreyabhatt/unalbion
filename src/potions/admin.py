from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PotionInput

@admin.register(PotionInput)
class PotionInputAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'updated_at')
        }),
        ('Herbs', {
            'fields': ('agaric', 'comfrey', 'burdock', 'teasel', 'foxglove', 'mullein', 'yarrow')
        }),
        ('Animal Products', {
            'fields': (
                'cow_milk', 'goat_milk', 'sheep_milk',
                'cow_butter', 'goat_butter', 'sheep_butter',
                'hen_eggs', 'goose_eggs'
            )
        }),
        ('Schnapps & Brews', {
            'fields': ('potato_schnapps', 'corn_hooch', 'pumpkin_moonshine')
        }),
        ('Enchantment Materials', {
            'fields': ('animal_remains',)
        }),
        ('Potion Sale Prices (collapsed)', {
            'classes': ('collapse',),
            'fields': [field.name for field in PotionInput._meta.get_fields()
                       if field.name.startswith('T') and '_' in field.name]
        }),
    )
