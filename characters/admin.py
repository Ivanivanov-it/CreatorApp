from django.contrib import admin

from characters.models import Character


# Register your models here.

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name','slug','title','attack','defense','hp','type','display_roles','image_url','creator_name']

    def display_roles(self,obj):
        return ", ".join(role.role for role in obj.roles.all())

    display_roles.short_description = 'Roles'

    def creator_name(self,obj):
        return obj.creator.username if obj.creator else ''

    creator_name.short_description = 'Creator'