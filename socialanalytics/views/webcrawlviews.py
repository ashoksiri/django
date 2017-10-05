# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import rest_framework_mongoengine.viewsets as mongoviewsets
from socialanalytics.serializers import NewsSerializer,StandardResultsSetPagination
from django.core.cache import cache
from datetime import date, datetime, timedelta
from socialanalytics.utils import refresh_data
from rest_framework.response import Response
from socialanalytics.utils import filtermodels
from dateutil import parser
from socialanalytics.models import News
from django.http import JsonResponse
from rest_framework import status

from django.shortcuts import render


current_date = int(datetime.now().date().strftime("%S"))


class NewsLiveData(mongoviewsets.GenericViewSet):

    """
       This Will Retrive the Live News from The Twitter Api Matched with Search Keyword

    """

    def list(self,request,searchKey):
        data = []
        if searchKey and len(searchKey) > 0:
            data = cache.get(searchKey + "_news", None)
            data = data if data else refresh_data.load_key_data(searchKey, "news")
            return Response(data)
        else:
            return Response(data)


    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request, searchKey)



class NewsHistoryData(mongoviewsets.ReadOnlyModelViewSet):
    """
            This View will return News from Database matched with searchKey and b/w the give date range.

    """

    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        newss = []

        if searchKey is not None and len(searchKey) >0 :
            from_date = self.request.GET.get('from_date', '')
            to_date   = self.request.GET.get('to_date', '')
            subkey    = self.request.GET.get('subkey', None)
            sentiment = self.request.GET.get('sentiment',None)
            news_key = searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(to_date) + '_newsdata'


            if (sentiment is not None and sentiment != '') and (subkey is None or subkey == ''):
                newsfilter = filtermodels.getpipeline("news", searchKey, from_date, to_date)
                newsfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                newss = [n for n in News.objects.aggregate(*newsfilter, allowDiskUse=True)]
                return newss

            if (subkey is not None and subkey != '') and (sentiment is not None and sentiment != ''):
                newsfilter = filtermodels.getpipeline("news", searchKey, from_date, to_date)
                newsfilter[0].get('$match').__setitem__('description_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})
                newsfilter[0].get('$match').__setitem__('polarity.key', {'$eq': sentiment})
                newss = [n for n in News.objects.aggregate(*newsfilter, allowDiskUse=True)]
                return newss

            if subkey is not None and subkey != '':

                pipeline = filtermodels.getpipeline(
                    source="news",
                    key=searchKey,
                    from_date=from_date,
                    to_date=to_date)
                pipeline[0].get('$match').__setitem__('description_parsed',{'$regex':r'\b{}\b'.format(subkey),'$options':'i'})
            else:
                pipeline = filtermodels.getpipeline(
                    source="news",
                    key=searchKey,
                    from_date=from_date,
                    to_date=to_date)

            newss = [news for news in News.objects.aggregate(*pipeline,allowDiskUse=True)]

            if len(newss) == 0:
                news = cache.get(news_key)
                if news:
                    return news
                newss = refresh_data.load_key_data(searchKey,"news")
                news =  filtermodels.filterwithsubkey(data = newss,subkey = subkey,source="news",from_date=from_date,to_date=to_date)
                cache.set(news_key, news)
                return news
            else:
                return newss
        else:
            return newss

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(NewsHistoryData, self).dispatch(request, *args, **kwargs)


class NewsAggregation(mongoviewsets.GenericViewSet):
    """
            This view Will Get the date wise frequency of records along with the Total Count

    """
    def list(self,request,searchKey):
        if searchKey is not None and len(searchKey) > 0:
            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey = self.request.GET.get('subkey', None)

            if subkey is not None and subkey != '':
                pipeline = filtermodels.getpipelinewithaggregation("news",searchKey,from_date,to_date)
                pipeline[0].get('$match').__setitem__('description_parsed', {'$regex': r'\b{}\b'.format(subkey)})
            else :
                pipeline = filtermodels.getpipelinewithaggregation("news", searchKey, from_date, to_date)
            newss = [v for v in News.objects.aggregate(*pipeline,allowDiskUse=True)]
            totalcount = [r.get('count') for r in newss]
            return Response({"totalcount": sum(totalcount), "data": newss})
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
            return super(NewsAggregation, self).dispatch(request, *args, **kwargs)


