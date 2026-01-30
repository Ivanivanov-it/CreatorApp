from django.db import models
from django.utils.text import slugify

# Create your models here.

from common.models import TimeStampModel, Role

from characters.models import Character


class Partner(TimeStampModel):
    name = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100,unique=True)
    roles = models.ManyToManyField(Role,related_name='partners')
    power = models.IntegerField(default=0)
    description = models.TextField()
    image_url = models.URLField(blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True,max_length=100)
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="partners"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.title}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name