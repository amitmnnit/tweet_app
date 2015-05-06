from django.conf.urls import patterns, include, url
from sse_wrapper.views import EventStreamView
from useraccount.views import *
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^tweet/$', tweet),
    url(r'^mytweets/$', mytweets),
    url(r'^followusers/$', followusers),
    url(r'^follow/(?P<user_id>\d+)/?$', follow, name='follow_user'),

    url(r'^sse/(?P<channel_extension>[\w]+)/$', EventStreamView.as_view(channel='sse'), name='sse'),
)