from django.contrib import admin
from .models import FishingBaitData


@admin.register(FishingBaitData)
class FishingBaitDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'worm_price', 't1_price', 't3_price', 't5_price')
    list_filter = ('user',)
    search_fields = ('user__username',)
