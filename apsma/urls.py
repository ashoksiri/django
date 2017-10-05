from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from socialanalytics.views import *
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from usermanage import urls as usermanagement_urls

schema_view = get_schema_view(title='Apsma API')


# We use a single global DRF Router that routes views from all apps in project
router = routers.DefaultRouter()

#router.register(r'youtube-live/(?P<searchKey>.+)'     , YoutubeLiveData     , base_name = "Youtube Live Data")
#router.register(r'news-live/(?P<searchKey>.+)'        , NewsLiveData        , r"news-live")
#router.register(r'facebook-live/(?P<searchKey>.+)'    , FacebookLiveData    , r"facebook-live")
#router.register(r'twitter-live/(?P<searchKey>.+)'     , TwitterLiveData     , r"twitter-live")
router.register(r'twitter_gis-live/(?P<searchKey>.+)' , Twitter_gis_data    , r"twitter_gis-live")
router.register(r'youtube-history/(?P<searchKey>.+)'  , YoutubeHistoryData  , r"youtube-history")
router.register(r'news-history/(?P<searchKey>.+)'     , NewsHistoryData     , r"news-history")
router.register(r'facebook-history/(?P<searchKey>.+)' , FaceokHistoryData   , r"facebook-history")
router.register(r'twitter-history/(?P<searchKey>.+)'  , TwitterHistoryData  , r"twitter-history")
router.register(r'facebook-agg/(?P<searchKey>.+)'     , FacebookAggregation , r'facebook-agg')
router.register(r'twitter-agg/(?P<searchKey>.+)'      , TwitterAggregation  , r'twitter-agg')
router.register(r'news-agg/(?P<searchKey>.+)'         , NewsAggregation     , r'news-agg')
#router.register(r'youtube-agg/(?P<searchKey>.+)'      , YoutubeAggregation  , r"youtube-agg"),
router.register(r'wordcloud/(?P<searchKey>.+)'        , Polaritywords       , r'wordcloud')
router.register(r'tweets/(?P<searchKey>.+)'           , Tweets              , r'tweets'),
router.register(r'sentiment/(?P<searchKey>.+)'        , GetSentiment , r'getsentiment'),
router.register(r'topics/(?P<searchKey>.+)'           , Topics , r'topics'),
router.register(r'searchfeed/(?P<searchKey>.+)/(?P<subKey>.+)', searchFeed , r'search'),
router.register(r'searchfeedwithSentiment/(?P<searchKey>.+)/(?P<sentiment>.+)', searchFeedWithSentiment , r'searchsentiment'),

router.register(r'twitterstatistics/(?P<searchKey>.+)',TwitterStatisitcs,r'twitterstatistics')
router.register(r'trendingtweets/(?P<searchKey>.+)',TrendingTweets,r'trendindtweets')
router.register(r'trendinghashtags/(?P<searchKey>.+)',TrendingHashTags,r'trendinghashtags')


"""
    Youtube Individual Page Services
"""
# router.register(r'getstatistis/(?P<searchKey>.+)',GetStatistcs,r'statistics')
# router.register(r'videobycategory/(?P<searchKey>.+)/(?P<categoryId>.+)',GetVideosByCategory,r'videobycategory')
# router.register(r'videobypolarity/(?P<searchKey>.+)',GetVideosByPolarity,r'videobypolarity')
# router.register(r'videobychannel/(?P<searchKey>.+)/(?P<channelId>.+)',GetVideosByChannel,r'videobychannel')
# router.register(r'videobysentiment/(?P<searchKey>.+)/(?P<sentiment>.+)',GetVideoBySentiment,r'videobysentiment')
# router.register(r'videobysubkey/(?P<searchKey>.+)/(?P<subkey>.+)',GetVideoBySubKey,r'videobysubkey')
# router.register(r'videostats/(?P<videoId>.+)',GetVideoStats,r'videostats')



urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', index, {}, name='index'),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title='APSMA')),
    url(r'^api/usermanage/',include(usermanagement_urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),


]


