from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from common.models import TimeStampModel, Role


# Create your models here.

class Character(TimeStampModel):
    class HeroType(models.TextChoices):
        ALIEN = 'ALIEN', 'ALIEN'
        HERO = 'HERO', 'HERO'
        GOD = 'GOD','GOD',
        DEMON = 'DEMON','DEMON'
        TIME_TRAVELER = 'TIME TRAVELER', 'TIME TRAVELER'
        VILLAIN = 'VILLAIN', 'VILLAIN'
        ANGEL = 'ANGEL', 'ANGEL'
        OTHER = 'OTHER', 'OTHER'



    name = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100,unique=True)
    type = models.CharField(choices=HeroType.choices,default=HeroType.OTHER)
    attack = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(100)])
    defense = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(100)])
    hp = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(100)])
    roles = models.ManyToManyField(Role, related_name='characters')
    description = models.TextField()
    slug = models.SlugField(max_length=100,unique=True,blank=True)
    image_url = models.URLField(blank=True,null=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.title}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name