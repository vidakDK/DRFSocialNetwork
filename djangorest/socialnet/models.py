from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class SocialnetUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance=None, created=False, **kwargs):
        if created:
            SocialnetUser.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance=None, **kwargs):
        instance.profile.save()


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100, blank=True, default='')
    creator = models.ForeignKey(SocialnetUser, related_name='posts', on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['number_of_likes']

    def __str__(self):
        return "Created at='{}', Number of likes={}, Content='{}'".format(
            self.created, self.number_of_likes, self.content)
