from django.conf import settings
from django.db import models

from users.models import User


class Profile(models.Model):
    class Meta:
        ordering = ['-id']

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Dictionaries
    # default_dictionnary