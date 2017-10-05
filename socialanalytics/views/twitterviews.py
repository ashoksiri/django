# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.cache import cache
import rest_framework_mongoengine.viewsets as mongoviewsets
from socialanalytics.serializers import *
from socialanalytics.utils import refresh_data,twitterUtils,filtermodels,topRecords
from socialanalytics.models.twittermodels import Tweet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from dateutil import parser
from mongoengine.queryset.visitor import Q
from datetime import date, datetime, timedelta
from django.shortcuts import redirect
from collections import OrderedDict


tutils = twitterUtils.TwitterUtils()
current_date = int(datetime.now().date().strftime("%S"))


class TwitterLiveData(mongoviewsets.GenericViewSet):
    """
        This Will Retrive the Live Tweets from The Twitter Api Matched with Search Keyword

    """
    def list(self,request,searchKey):
        data = []
        if searchKey and len(searchKey) > 0:
            data = cache.get(searchKey + "_twitter", None)
            data = data if data else refresh_data.load_key_data(searchKey, "twitter")
            return Response(data)
        else:
            return Response(data)

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request,searchKey)

class Twitter_gis_data(mongoviewsets.GenericViewSet):

    """
        This View Will Return The Tweets with Gis Information like longitude, latitude

        and user information like username, userid, screen_name and tweet.

    """
    #serializer_class = TweetGisSerializer

    def list(self,request,searchKey):
        data = []
        zone = self.request.GET.get('zone', None)
        if searchKey and len(searchKey) > 0 and zone is not None:
            data = cache.get(searchKey + "_gis")
            data = data if data is not None else filtermodels.gettwittergisfields(searchKey,
                                                                                  tutils.getTweetswithAll(searchKey=searchKey,count=40),
                                                                                  zone=zone)
            return Response(data)

        elif searchKey and len(searchKey) > 0:
            data = cache.get(searchKey + "_gis")
            data = data if data is not None else filtermodels.gettwittergisfields(searchKey,
                                                                                  tutils.getTweetswithAll(searchKey=searchKey,count=40))
            return Response(data)
        else:
            return Response(data)

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request,searchKey)

class Tweets(mongoviewsets.GenericViewSet):
    """
        This View will Return the Tweets ,hashtags, top tweets, popular words from Database matched with search Keyword and  b/w the given date range.

        if the new keyword is given or to_date is current_date then the data will pull from live.


    """
    def get_queryset(self):
        return self.list(self.request,self.kwargs['searchKey'])

    def list(self,request,searchKey):
        tweets = []
        if searchKey is not None and len(searchKey) > 0:
            from_date = self.request.GET.get('from_date', '')
            to_date = self.request.GET.get('to_date', '')

            if searchKey not in Tweet.objects.distinct('searchKey'):
                refresh_data.load_key_data(searchKey, 'twitter')

            # if to_date is not '' and parser.parse(to_date).date().__str__() == date.today().__str__():
            #     refresh_data.load_key_data(searchKey, 'twitter')

            pipeline = filtermodels.getpipeline(source="twitter", key=searchKey, from_date=from_date, to_date=to_date,limit=100)
            tweets = [tweet for tweet in Tweet.objects.aggregate(*pipeline,allowDiskUse=True)]

            if len(tweets) == 0:
                return Response([])
            else:
                return JsonResponse(topRecords.getTweetsFilters(tweets),safe=False)
        else:
            return Response([])

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(Tweets, self).dispatch(request, *args, **kwargs)

class TwitterHistoryData(mongoviewsets.ReadOnlyModelViewSet):
        """
            This View will return Tweets matched with searchKey and b/w the give date range.

        """
        serializer_class = TwitterSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):

            searchKey = self.kwargs['searchKey']
            tweets = []

            if searchKey is not None and len(searchKey) > 0:
                from_date = self.request.GET.get('from_date', '')
                to_date = self.request.GET.get('to_date', '')
                subkey = self.request.GET.get('subkey', None)
                sentiment = self.request.GET.get('sentiment', None)
                twitter_key = searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(
                    to_date) + '_twitterdata'

                if (sentiment is not None and sentiment != '') and (subkey is None or subkey == ''):
                    twitterfilter = filtermodels.getpipeline("twitter", searchKey, from_date, to_date)
                    twitterfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                    tweets = [n for n in Tweet.objects.aggregate(*twitterfilter, allowDiskUse=True)]
                    return tweets

                if (subkey is not None and subkey != '') and (sentiment is not None and sentiment != ''):
                    twitterfilter = filtermodels.getpipeline("twitter", searchKey, from_date, to_date)
                    twitterfilter[0].get('$match').__setitem__('text_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})
                    twitterfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                    tweets = [n for n in Tweet.objects.aggregate(*twitterfilter, allowDiskUse=True)]
                    return tweets



                if subkey is not None and subkey != '':

                    pipeline = filtermodels.getpipeline(
                        source="twitter",
                        key=searchKey,
                        from_date=from_date,
                        to_date=to_date)
                    pipeline[0].get('$match').__setitem__('text_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})

                    tweets = [tweet for tweet in Tweet.objects.aggregate(*pipeline, allowDiskUse=True)]
                    return tweets
                else:
                    pipeline = filtermodels.getpipeline(
                        source="twitter",
                        key=searchKey,
                        from_date=from_date,
                        to_date=to_date)
                    tweets = [tweet for tweet in Tweet.objects.aggregate(*pipeline, allowDiskUse=True)]


                if len(tweets) == 0:
                    tweets = cache.get(twitter_key)
                    if tweets:
                        return tweets
                    tweets = refresh_data.load_key_data(searchKey, "twitter")
                    tweets = filtermodels.filterwithsubkey(data=tweets, subkey=subkey, source="twitter",
                                                          from_date=from_date, to_date=to_date)
                    cache.set(twitter_key, tweets)
                    return tweets
                else:
                    return tweets
            else:
                return tweets

        def dispatch(self, request, *args, **kwargs):
            # check if there is some video onsite
            to_date = request.GET.get('to_date', '')
            if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
                content = {'error':'GraterThan current_date not Allowed','status_code':status.HTTP_400_BAD_REQUEST}
                return JsonResponse(content,status=status.HTTP_400_BAD_REQUEST,safe=False)
            else:
                return super(TwitterHistoryData, self).dispatch(request, *args, **kwargs)

class TwitterAggregation(mongoviewsets.GenericViewSet):

    """

        This View will return the total count and date wise frequency of tweets from the database matched with the searchKey and b/w the date range give.


    """

    def list(self,request,searchKey):


        if searchKey is not None and len(searchKey) > 0:
            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey = self.request.GET.get('subkey', None)
            if subkey is not None and subkey != '':
                pipeline = filtermodels.getpipelinewithaggregation("twitter",searchKey,from_date,to_date)
                pipeline[0].get('$match').__setitem__('text_parsed', {'$regex': r'\b{}\b'.format(subkey)})
            else :
                pipeline = filtermodels.getpipelinewithaggregation("twitter", searchKey, from_date, to_date)

            tweets = [v for v in Tweet.objects.aggregate(*pipeline,allowDiskUse=True)]
            totalcount = [r.get('count') for r in tweets]
            return Response({"totalcount": sum(totalcount), "data": tweets})
        else:
            return Response({"totalcount": 0, "data": []})


    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request,searchKey)

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(TwitterAggregation, self).dispatch(request, *args, **kwargs)

class TrendingTweets(mongoviewsets.ReadOnlyModelViewSet):

    serializer_class = TrendingTweetSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):

        searchKey = self.kwargs['searchKey']
        if searchKey is not None and len(searchKey) > 0:
            from_date = self.request.GET.get('from_date', '')
            to_date   = self.request.GET.get('to_date', '')
            daterange = filtermodels.getdaterange(from_date,to_date)
            data = Tweet.objects(Q(searchKey=searchKey)&
                          Q(created_at__gte=daterange.get('from_date')) &
                          Q(created_at__lte=daterange.get('to_date'))).order_by('-retweet_count')
            return data

class TrendingHashTags(mongoviewsets.GenericViewSet):

    #pagination_class = StandardResultsSetPagination

    def list(self,request,searchKey):
        return self.get_queryset()

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        if searchKey is not None and len(searchKey) > 0:
            from_date = self.request.GET.get('from_date', '')
            to_date = self.request.GET.get('to_date', '')
            daterange = filtermodels.getdaterange(from_date, to_date)
            data = Tweet.objects(Q(searchKey=searchKey) &
                                 Q(created_at__gte=daterange.get('from_date')) &
                                 Q(created_at__lte=daterange.get('to_date'))).item_frequencies('user.screen_name')
            from operator import itemgetter
            top_tags = sorted(data.items(), key=itemgetter(1), reverse=True)[:10]
            return Response({'count':data.__len__(),'users':top_tags})


class TwitterStatisitcs(mongoviewsets.GenericViewSet):

    def list(self,request,searchKey):
        return self.get_queryset()

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        print "HashTags"
        if searchKey is not None and len(searchKey) > 0:
            from_date = self.request.GET.get('from_date', '')
            to_date = self.request.GET.get('to_date', '')
            #pipeline = filtermodels.getTwitterPipelines(searchKey,from_date,to_date)
            data = [t for t in Tweet.objects.aggregate(*[{'$match':{'searchKey':searchKey}},{'$project':{'id':'$tweetid','text':'$text'}},{'$limit':10}])]
            return Response(data)