from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(models.Model):
    class RoleType(models.TextChoices):
        ATTACK = 'ATTACK', 'ATTACK'
        DEFEND = 'DEFEND', 'DEFEND'
        HEAL = 'HEAL', 'HEAL'
        BUFF = 'BUFF', 'BUFF'
        SUPPORT = 'SUPPORT', 'SUPPORT'
        SEARCH = 'SEARCH', 'SEARCH'

    role = models.CharField(
        max_length=20,
        choices=RoleType.choices,
        unique=True,
    )

    def __str__(self):
        return self.role