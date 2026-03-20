from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to="images/profile_pictures",blank=True,null=True)



