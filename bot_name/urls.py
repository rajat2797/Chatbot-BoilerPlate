from django.conf.urls import patterns, include, url
from django.contrib import admin
from chatbot.views import *

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^facebook_auth/?$', MyChatBotView.as_view(), name='fb_callback'),
)
