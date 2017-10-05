
from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import pagination
from socialanalytics.models import Tweet,Facebook,News,Video,TweetGis

class FacebookSerializer(mongoserializers.DocumentSerializer):

    class Meta:
        model = Facebook
        fields =  '__all__'

class TwitterSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'

class TrendingTweetSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Tweet
        fields = ('text','retweet_count')


class TweetGisSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = TweetGis
        fields = "__all__"

class NewsSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = News
        fields = '__all__'

class YoutubeSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
