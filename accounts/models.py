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
    class Meta:
        verbose_name_plural = 'CustomUser'

class Connection(models.Model):
    following = models.ForeignKey(CustomUser,
                                  related_name = 'following', on_delete = models.CASCADE)
    followed = models.ForeignKey(CustomUser,
                                 related_name = 'followed', on_delete = models.CASCADE)

    def __str__(self):
        return f"'{self.following.username}' follows '{self.followed.username}'"
