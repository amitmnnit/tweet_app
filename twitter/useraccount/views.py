from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from useraccount.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from useraccount.models import *
from django.contrib.auth.models import User
import datetime
import json
from django.core import serializers
from sse_wrapper.events import send_event

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from useraccount.tasks import tweet_on_follower_wall

from django.core.signals import request_finished
from django.dispatch import receiver

@csrf_protect
def register(request):
    """
    user registration form.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            follow = FollowUser.objects.create(profile=user)
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    """
    show registration status.
    """
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    "logout from home"
    logout(request)
    return HttpResponseRedirect('/')
 
def get_tweets(users):
    """
    function to return tweets for a user to be displayed on wall.
    """
    date = (datetime.datetime.today()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    tweets = []
    for user in users:
        tweets+=user.tweets.filter(tweeted_at__gte=date)
    tweets.sort(key=lambda x: x.tweeted_at, reverse=True)
    for tweet in tweets:
        tweet.user = tweet.profile.all()[0]
        tweet.tweeted_at = tweet.tweeted_at
    return tweets

@login_required
def mytweets(request):
    """
    all tweets which user tweeted can be seen here.
    """
    date = (datetime.datetime.today()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    user_followed=list(request.user.followuser.follow.all().values_list('id', flat=True).distinct())
    user_followed.append(request.user.id)
    tweets = request.user.tweets.filter(tweeted_at__gte=date).order_by('-tweeted_at')
    return render_to_response(
    'home.html',
    { 'user': request.user, 'tweets': tweets, 'mytweets':True, 'channel_extension': request.user.id}
    )

@login_required
def follow(request, user_id):
    """
    follow any new user to see his all tweets.
    """
    follow_user = User.objects.get(id=user_id)
    request.user.followuser.follow.add(follow_user)
    return HttpResponseRedirect(reverse('useraccount.views.home'))

@login_required
def home(request):
    """
    home page where user can see tweets posted by followed ones.
    """
    user_followed=list(request.user.followuser.follow.all().values_list('id', flat=True).distinct())
    user_followed.append(request.user.id)
    tweets = get_tweets(request.user.followuser.follow.all())
    return render_to_response(
    'home.html',
    { 'user': request.user, 'tweets': tweets, 'mytweets':False, 'channel_extension': request.user.id}#,contenxt_instance = RequestContext(request)
    )


@login_required
def followusers(request):
    """
    unfollowed user list who can be followed.
    """
    user_followed=list(request.user.followuser.follow.all().values_list('id', flat=True).distinct())
    user_followed.append(request.user.id)
    users = User.objects.exclude(id__in=user_followed)
    return render_to_response(
    'followusers.html',
    { 'user': request.user, 'users':users}
    )

@login_required
def tweet(request):
    """
    tweet some thing that can be seen by others.
    """
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = Tweet.objects.create(tweet=form.cleaned_data['tweet'])
            tweet.profile.add(request.user)
            followers = request.user.followers.all()
            for follower in followers:
                tweet_on_follower_wall.delay(follower.profile, tweet)
            return HttpResponseRedirect('/home/')
    else:
        form = TweetForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'tweet.html',
    variables,
    )