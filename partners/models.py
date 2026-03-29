from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Create your models here.

from common.models import TimeStampModel, Role, CombatStatModel

from characters.models import Character


class Partner(TimeStampModel,CombatStatModel):
    name = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100,unique=True)
    roles = models.ManyToManyField(Role,related_name='partners')
    description = models.TextField()
    image_url = CloudinaryField('image',null=True,blank=True)
    slug = models.SlugField(unique=True,blank=True,max_length=100)
    character = models.ManyToManyField(Character,related_name='partners',blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partners')
    card_theme = models.ForeignKey('cards.Card',on_delete=models.SET_NULL,null=True,blank=True,related_name='partners')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.title}")

        # if not self.image_url:
        #     self.image_url = f"{settings.STATIC_URL}images/partner.png"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name