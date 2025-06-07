from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
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

    # Must be the type same as the primary key used by
    # the CustomUser id.
    following = ArrayField(models.BigIntegerField(),
                           blank = True,
                           default = list)
    follower = ArrayField(models.BigIntegerField(),
                          blank = True,
                          default = list)
    class Meta:
        verbose_name_plural = 'CustomUser'
