from email.policy import default
from tokenize import blank_re
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likers = models.ManyToManyField(User, blank=True, related_name='likers')
    does_like = models.BooleanField(default=False)
    likes = 0

    @property
    def returnlikes(self):
        likes = len(self.likers.all())
        if likes==0:
            return 'No Likes :('
        if likes==1:
            return '1 Like!'
        return str(likes)+' Likes!'

    def __str__(self) -> str:
        return self.author.username + " - " + self.body[:10] + "..."
    
    def __repr__(self) -> str:
        return self.body[:10] + "..."


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE, verbose_name='user', related_name='profile')
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    birth_date = models.DateField(null=True)
    picture = models.ImageField(blank=True, null=True, default='uploads/profile_pictures/default.jpg', upload_to='uploads/profile_pictures')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self) -> str:
        return self.user.profile.name



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('üser profile created')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print('üser profile created')




















