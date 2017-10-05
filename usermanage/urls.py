"""authenticationpractice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.models import User, Group
admin.autodiscover()
from usermanage import views
from usermanage.views import *

from rest_framework import serializers, routers, permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register('login', LoginView)
router.register('addclient', ClientView),
router.register('adduser', UserSave)
router.register('addpreference', SavePreferences),
router.register('addchannel',SaveChannelsPages),
# router.register('getclients',GetClients)

# router.register('savekeyword',KeywordData)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url (r'^', include (router.urls)),
    url (r'^$', Home.as_view ()),

    url(r'^getclients/$',GetClients.as_view()),
    url(r'^updateclient/(?P<pk>\d+)/$', UpdateClient.as_view(), name='client_update'),

    url(r'^addkeyword/$',KeywordData.as_view()),
    url(r'^getkeywords/(?P<user_id>\d+)/$',RetrieveUserKeywordData.as_view()),
    url(r'^updatekeyword/(?P<keyword_id>\d+)/$', UpdateKeywordView.as_view(), name='keyword_partial_update'),
    url(r'^deletekeyword/(?P<keyword_id>\d+)/$', DeleteKeywordView.as_view(), name='channel_partial_update'),

    url(r'^updatechannel/(?P<channel_id>\d+)/$', UpdateChannelView.as_view(), name='channel_partial_update'),
    url(r'^deletechannel/(?P<channel_id>\d+)/$', DeleteChannelView.as_view(), name='channel_partial_update'),


    url(r'^getpreferences/(?P<user_id>\d+)/$',RetrievePreferences.as_view()),

    url('^getchannels/(?P<user_id>\d+)/$',RetrieveChannelPages.as_view()),
    url('^getchanneldetails/(?P<user_id>\d+)/$',GetChannelPages.as_view()),

]



