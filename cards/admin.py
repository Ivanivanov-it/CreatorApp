from django.contrib import admin

from cards.models import Card


# Register your models here.

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name','border_color','border_style','background_color','image_border_color','image_border_style','accent_color','is_default','creator_name']

    def creator_name(self,obj):
        return obj.creator.username if obj.creator else ''

    creator_name.short_description = 'Creator'