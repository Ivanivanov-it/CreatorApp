from django.contrib import admin

from battle.models import BattleCharacter


# Register your models here.

@admin.register(BattleCharacter)
class BattleCharacterAdmin(admin.ModelAdmin):
    list_display = ["character_id","battle_id","base_hp","base_atk","base_def","buff_hp","buff_atk","buff_def","debuff_hp","debuff_atk","debuff_def","current_hp","current_atk","current_def"]
