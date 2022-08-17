from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Meta:
        ordering = ['-id']

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Dictionaries

    def __str__(self):
        return f"{self.user.email}"
