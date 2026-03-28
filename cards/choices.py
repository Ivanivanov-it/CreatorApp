from django.db import models


class BorderStyleChoices(models.TextChoices):
    SOLID = 'solid', 'Solid'
    DASHED = 'dashed', 'Dashed'
    DOTTED = 'dotted', 'Dotted'
    DOUBLE = 'double', 'Double'
    GROOVE = 'groove', 'Groove'
    RIDGE = 'ridge', 'Ridge'
    INSET = 'inset', 'Inset'
    OUTSET = 'outset', 'Outset'
    NONE = 'none', 'None'
