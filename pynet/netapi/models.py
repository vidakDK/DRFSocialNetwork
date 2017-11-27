from django.db import models
from django.contrib.auth.models import User
from votes.managers import VotableManager


class Post(models.Model):
    content = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)
    # post_votes = models.ForeignKey(PostAction, on_delete=models.CASCADE)
    # votes = VotableManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{}. Owner='{}', NumLikes={}, Content='{}'".format(self.id,
                                                                  self.owner.username,
                                                                  self.number_of_likes,
                                                                  self.content)


class PostAction(models.Model):
    POST_ACTION_TYPES = ((1, 'like'), (0, 'unlike'))
    action_type = models.IntegerField(choices=POST_ACTION_TYPES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['post_id']
