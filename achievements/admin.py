from django.contrib import admin

from achievements.models import Achievement


# Register your models here.

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name','type','threshold','icon']
