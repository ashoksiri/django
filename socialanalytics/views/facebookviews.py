# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import *
from rest_framework.response import Response
from rest_framework import status
from socialanalytics.serializers import StandardResultsSetPagination,FacebookSerializer
from socialanalytics.models import Facebook
from django.core.cache import cache
from socialanalytics.utils import refresh_data
import rest_framework_mongoengine.viewsets as mongoviewsets
from socialanalytics.utils import filtermodels
from dateutil import parser
from datetime import date,datetime

current_date = int(datetime.now().date().strftime("%S"))

class FacebookLiveData(mongoviewsets.GenericViewSet):
    """
            This Will Retrive the Live posts from The Twitter Api Matched with Search Keyword

    """

    def list(self, request, searchKey):
        data = []
        try:
            if searchKey and len(searchKey) > 0:
                data = cache.get(searchKey + "_facebook", None)
                data = data if data else refresh_data.load_key_data(searchKey, "facebook")
        except Exception as e:
            print e.message
            return Response(data)

        return Response(data)

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request, searchKey)


"""
    View for Fetching Facebook History data from Database matching searchKey and given date range
"""

class FaceokHistoryData(mongoviewsets.ReadOnlyModelViewSet):

    """
        This View will return Tweets matched with searchKey and b/w the give date range.

    """
    serializer_class = FacebookSerializer
    lookup_field = 'postid'
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        searchKey = self.kwargs['searchKey']
        posts = []

        if searchKey is not None and len(searchKey) >0 :
            from_date = self.request.GET.get('from_date', '')
            to_date   = self.request.GET.get('to_date', '')
            subkey    = self.request.GET.get('subkey', None)
            sentiment = self.request.GET.get('sentiment',None)
            facebook_key = searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(to_date) + '_facebookdata'

            if (sentiment is not None and sentiment != '') and (subkey is None or subkey == ''):
                facebookfilter = filtermodels.getpipeline("facebook", searchKey, from_date, to_date)
                facebookfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                posts = [n for n in Facebook.objects.aggregate(*facebookfilter, allowDiskUse=True)]
                return posts


            if (subkey is not None and subkey != '') and (sentiment is not None and sentiment != ''):
                facebookfilter = filtermodels.getpipeline("facebook", searchKey, from_date, to_date)
                facebookfilter[0].get('$match').__setitem__('message_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})
                facebookfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                posts = [n for n in Facebook.objects.aggregate(*facebookfilter, allowDiskUse=True)]
                return posts




            if subkey is not None and subkey != '':

                pipeline = filtermodels.getpipeline(
                    source="facebook",
                    key=searchKey,
                    from_date=from_date,
                    to_date=to_date)
                pipeline[0].get('$match').__setitem__('message_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})
                posts = [post for post in Facebook.objects.aggregate(*pipeline, allowDiskUse=True)]
                return posts
            else:
                pipeline = filtermodels.getpipeline(
                    source="facebook",
                    key=searchKey,
                    from_date=from_date,
                    to_date=to_date)

            posts = [post for post in Facebook.objects.aggregate(*pipeline,allowDiskUse=True)]

            if len(posts) == 0:
                posts = cache.get(facebook_key)
                if posts:
                    return posts
                posts = refresh_data.load_key_data(searchKey,"facebook")
                posts =  filtermodels.filterwithsubkey(data = posts,subkey = subkey,source="facebook",from_date=from_date,to_date=to_date)
                cache.set(facebook_key, posts)
                return posts
            else:
                return posts
        else:
            return posts


    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(FaceokHistoryData, self).dispatch(request, *args, **kwargs)


class FacebookAggregation(mongoviewsets.GenericViewSet):

    """
        This view Will Get the date wise frequency of records along with the Total Count

    """

    def list(self,request,searchKey):

        if searchKey is not None and len(searchKey) > 0:
            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey = self.request.GET.get('subkey', None)
            if subkey is not None and subkey != '':
                pipeline = filtermodels.getpipelinewithaggregation("facebook",searchKey,from_date,to_date)
                pipeline[0].get('$match').__setitem__('message_parsed', {'$regex': r'\b{}\b'.format(subkey)})
            else :
                pipeline = filtermodels.getpipelinewithaggregation("facebook", searchKey, from_date, to_date)
            result = [r for r in Facebook.objects.aggregate(*pipeline,allowDiskUse=True)]
            totalcount = [r.get('count') for r in result]
            return Response({"totalcount": sum(totalcount), "data": result})
        else:
            return Response({"totalcount": 0, "data": []})


    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request, searchKey)

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(FacebookAggregation, self).dispatch(request, *args, **kwargs)
