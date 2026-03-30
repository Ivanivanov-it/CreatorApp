from django.contrib import admin
from enemies.models import Enemy


# Register your models here.


@admin.register(Enemy)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name','slug','title','attack','defense','hp','type','display_weakness','image_url','creator_name']

    def display_weakness(self,obj):
        return ", ".join(weakness.role for weakness in obj.weakness.all())

    display_weakness.short_description = 'Weakness'

    def creator_name(self,obj):
        return obj.creator.username if obj.creator else ''

    creator_name.short_description = 'Creator'