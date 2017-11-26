from django.db import models
from django.contrib.auth.models import User
from votes.managers import VotableManager


class Post(models.Model):
    content = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)
    post_votes = models.ForeignKey(PostAction, on_delete=models.CASCADE)

    class Meta:
        ordering = ['number_of_likes']


class PostAction(models.Model):
    POST_ACTION_TYPES = ('like', 'dislike')
    action_type = models.CharField(choices=POST_ACTION_TYPES)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
