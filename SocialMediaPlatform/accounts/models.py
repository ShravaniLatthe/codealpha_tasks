from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    followers = models.ManyToManyField(
        User,
        related_name="followers",
        blank=True
    )

    following = models.ManyToManyField(
        User,
        related_name="following",
        blank=True
    )

    def __str__(self):
        return self.user.username