from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['number_of_likes']
