from django.db import models
from django.contrib.auth.models import User
from time import sleep
from sse_wrapper.events import send_event
import json

class FollowUser(models.Model):
	profile = models.OneToOneField(User)
	follow = models.ManyToManyField(User, related_name='followers')
	followed_on = models.DateTimeField(auto_now_add=True)
	blocked = models.BooleanField(default=0)

class Tweet(models.Model):
    profile = models.ManyToManyField(User, related_name='tweets')
    tweeted_at = models.DateTimeField(auto_now_add=True)
    tweet = models.TextField(max_length=255)