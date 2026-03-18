from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    # image_url = models.URLField(blank=True,null=True)
    pass


