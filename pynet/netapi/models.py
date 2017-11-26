from django.db import models
from django.contrib.auth.models import User
from votes.managers import VotableManager


class Post(models.Model):
    content = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)
    votes = VotableManager()

    class Meta:
        ordering = ['number_of_likes']
