from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField

class CustomUser(AbstractUser):
    description = models.TextField(verbose_name = 'description',
                                   null = True,
                                   blank = True)
    photo = models.ImageField(verbose_name = 'photo',
                              null = True,
                              blank = True,
                              upload_to = 'images/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = 'CustomUser'
