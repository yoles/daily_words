from django.db import models

from profiles.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default=None)


class Dictionary(models.Model):
    profile = models.ForeignKey(Profile, related_name="dictionaries", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # words


class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="words")
    title = models.CharField(max_length=50)
    definition = models.TextField()
    is_known = models.BooleanField(default=False)
    last_played = models.DateField(null=True, blank=True)
