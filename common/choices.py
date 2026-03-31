from django.db import models

class CharacterType(models.TextChoices):
    ALIEN = 'ALIEN', 'ALIEN'
    HERO = 'HERO', 'HERO'
    GOD = 'GOD', 'GOD',
    DEMON = 'DEMON', 'DEMON'
    TIME_TRAVELER = 'TIME TRAVELER', 'TIME TRAVELER'
    VILLAIN = 'VILLAIN', 'VILLAIN'
    ANGEL = 'ANGEL', 'ANGEL'
    OTHER = 'OTHER', 'OTHER'

class BattleStatus(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    FINISHED = 'Finished', 'Finished'

class LogType(models.TextChoices):
    INFO = 'INFO', 'INFO'
    ATTACK = 'ATTACK', 'ATTACK'
    DEFEND = 'DEFEND', 'DEFEND'
    HEAL = 'HEAL', 'HEAL'
    SEARCH = 'SEARCH', 'SEARCH'

class AchievementType(models.TextChoices):
    FIRST_WIN = "first_win", "First Win"
    WIN_STREAK = "win_streak", "Win Streak"
    TOTAL_WINS = "total_wins", "Total Wins"
    TOTAL_BATTLES = "total_battles", "Total Battles"
    PERFECT_VICTORY = "perfect_victory", "Perfect Victory"
    PERFECT_LOSE = "perfect_lose", "Perfect Lose"
    FIRST_LOSE = "first_lose", "First Lose"
    TOTAL_LOSES = "total_loses", "Total Loses"
    FIRST_CHARACTER_CREATION = "first_character_creation", "First Character Creation"
    FIRST_PARTNER_CREATION = "first_partner_creation", "First Partner Creation"
    FIRST_ENEMY_CREATION = "first_enemy_creation", "First Enemy Creation"
    FIRST_CARD_CREATION = "first_card_creation", "First Card Creation"