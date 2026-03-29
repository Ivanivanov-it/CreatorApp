from django.contrib import admin

from partners.models import Partner


# Register your models here.

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name','slug','title','attack','defense','hp','display_characters','display_roles','image_url','creator_name']


    def display_characters(self,obj):
        return ", ".join(char.name for char in obj.character.all())

    def display_roles(self,obj):
        return ", ".join(role.role for role in obj.roles.all())

    display_roles.short_description = 'Roles'
    display_characters.short_description = 'Related Character'

    def creator_name(self,obj):
        return obj.creator.username if obj.creator else ''

    creator_name.short_description = 'Creator'
