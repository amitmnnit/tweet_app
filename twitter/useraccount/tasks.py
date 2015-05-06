import json
from celery import task
from sse_wrapper.events import send_event
from django.contrib.auth.models import User
import datetime

@task(serializer='pickle', queue='web', routing_key='web')
def tweet_on_follower_wall(follower, tweet):
    user_followed=list(follower.followuser.follow.all().values_list('id', flat=True).distinct())
    users = User.objects.filter(id__in=user_followed)
    data = [{'username':tweet.profile.all()[0].username, 'tweet':tweet.tweet, 'date':tweet.tweeted_at.strftime('%b %d, %Y %I:%M %P')}]
    send_event('myevent', json.dumps(data), 'sse/%s' % follower.id)
