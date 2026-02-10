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