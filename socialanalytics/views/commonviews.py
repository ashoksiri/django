
from django.shortcuts import redirect
from rest_framework.response import Response
import rest_framework.viewsets as viewsets
from socialanalytics.utils.topicutil import gettopics
from socialanalytics.utils.wordcloud import getPolarity
from datetime import date
from dateutil.parser import parse
from django.core.cache import cache
from socialanalytics.models import Tweet
from django.http import JsonResponse
import json

from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet,ReadOnlyModelViewSet
from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.fields import *
from mongoengine import Document

class SampleTopics(Document):
    searchKey = StringField()
    topics = StringField()

class TopicSerializer(DocumentSerializer):
    class Meta:
        model = SampleTopics
        fields = '__all__'

class TopicView(ModelViewSet):
    serializer_class = TopicSerializer
    queryset = SampleTopics.objects.all()

class TopicsDataView(GenericViewSet):
    def list(self, request, searchKey):
        data = []
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')

        if searchKey in SampleTopics.objects.distinct('searchKey'):

            return Response(json.loads(SampleTopics.objects(searchKey=searchKey)[0].topics))

        else:
            result = data if data else gettopics(searchKey=searchKey, from_date=from_date, to_date=to_date)

            data = {'searchKey': searchKey, 'topics': json.dumps(result)}
            serializer = TopicSerializer(data=data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
            else:
                print serializer.errors
            return Response(result)
            #return Response([])

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request, searchKey)


class Wordcloud(Document):
    searchKey = StringField()
    data      = StringField()

class WordCloudSerializer(DocumentSerializer):
    class Meta:
        model = Wordcloud
        fields = '__all__'


class WordCoudView(GenericViewSet):
    def list(self, request, searchKey):

        if searchKey in Wordcloud.objects.distinct('searchKey'):


            return Response(json.loads(Wordcloud.objects(searchKey=searchKey)[0].data))
        else:
            return Response([])

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        return self.list(self.request, searchKey)

class WordCloudData(ModelViewSet):
    queryset = Wordcloud.objects.all()
    serializer_class = WordCloudSerializer

def handle404(request):
    """
        This view Responsible for Page Not Found

        If Url Nor found the url will be redirected to /api/.
    """
    return redirect('/api/')


def index(request):
    """

        This url will be redirected to /api/ when root url called.
    """
    return JsonResponse({'home':'Welcome'})
    #return redirect('/api/')

class Topics(viewsets.GenericViewSet):

    """
        This is Responsible for getting Topics, trends from 4 channels from given date range.

    """

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        self.list(self.request,searchKey)

    def list(self,request,searchKey):

        if searchKey is not None and len(searchKey) > 0:

            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey  = request.GET.get('subkey',None)
            subkey = None if subkey == '' else subkey

            """
                If to_date is current date then live data will be push to Database and topics willbe generated
            """
            if to_date != '' and \
                            parse(to_date).date().__str__() == date.today().__str__() \
                    or searchKey not in Tweet.objects.distinct('searchKey'):

                    """
                        Loading data to Database.
                    """
                    #refresh_data.load_all_dala(searchKey)
                    cache.set(searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(to_date) + '_topics',None)

            data = cache.get(searchKey +'_'+str(subkey)+'_'+str(from_date)+'_'+str(to_date) + '_topics')

            data = data if data else gettopics(searchKey=searchKey, from_date=from_date, to_date=to_date)
            return Response(data)
        else:
            return Response([])

class Polaritywords(viewsets.GenericViewSet):

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        self.list(self.request, searchKey)

    def list(self, request, searchKey):

        if searchKey is not None and len(searchKey) > 0:

            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey = request.GET.get('subkey',None)
            subkey = None if subkey == '' else subkey

            """
                If to_date is current date then live data will be push to Database and topics willbe generated
            """
            if to_date != '' and \
                            parse(to_date).date().__str__() == date.today().__str__() \
                    or searchKey not in Tweet.objects.distinct('searchKey'):
                """
                    Loading data to Database.
                """
                None
                #refresh_data.load_all_dala(searchKey)
                #cache.set(searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(to_date) + '_wordcloud', None)
            data = cache.get(searchKey +'_'+str(subkey)+'_'+str(from_date)+'_'+str(to_date) + '_wordcloud')
            data = data if data else getPolarity(q=searchKey,from_date=from_date,to_date=to_date)

            return Response(data)
            # if searchKey in Wordcloud.objects.distinct('searchKey'):
            #
            #
            #     return Response(json.loads(Wordcloud.objects(searchKey=searchKey)[0].data))
            # else:
            #     #data = cache.get(searchKey + '_wordcloud')
            #     data = []
            #     data = data if data else getPolarity(q=searchKey, from_date=from_date, to_date=to_date)
            #     result = {'searchKey':searchKey,'data':json.dumps(data)}
            #     serializer = WordCloudSerializer(data= result)
            #     if(serializer.is_valid(raise_exception=False)):
            #         serializer.save()
            #     else:
            #         serializer.errors
            #
            #     return Response(data)
        else:
            return Response([])

def test(request,searchKey):
    return JsonResponse([1,2,3],safe=False)

# class SampleView(viewsets.GenericViewSet):
#
#     pagination_class = StandardResultsSetPagination
#     def get_queryset(self):
#         return self.list(self.request)
#
#     def list(self,request):
#
#         searchKey = self.request.GET.get('q', '')
#
#         if searchKey is None or searchKey is '':
#             return []
#
#         from_date = self.request.GET.get('from_date', '')
#         to_date = self.request.GET.get('to_date', '')
#
#         facebookpipeline = filtermodels.getpipeline(source="facebook", key=searchKey, from_date=from_date,
#                                                     to_date=to_date, limit=10)
#         twitterpipeline = filtermodels.getpipeline(source="twitter", key=searchKey, from_date=from_date,
#                                                    to_date=to_date, limit=10)
#         newspipeline = filtermodels.getpipeline(source="news", key=searchKey, from_date=from_date, to_date=to_date,
#                                                 limit=10)
#         youtubepipeline = filtermodels.getpipeline(source="youtube", key=searchKey, from_date=from_date,
#                                                    to_date=to_date, limit=10)
#
#         queryset1 = Facebook.objects.all()
#         queryset2 = Tweet.objects.all()
#         queryset3 = Video.objects.all()
#
#         context = {
#             "request": request,
#         }
#
#         files_serializer = FacebookSerializer(queryset1, many=True, context=context)
#
#         video_serializer = YoutubeSerializer(queryset3, many=True, context=context)
#
#         dirs_serializer = TwitterSerializer(queryset2, many=True, context=context)
#
#         response = (files_serializer.data , video_serializer.data , dirs_serializer.data)
#
#         pagination1 = self.paginate_queryset(response)
#
#         # pagination3 = self.paginate_queryset(queryset3)
#         #
#         # pagination2 = self.paginate_queryset(queryset2)
#
#         response2 = self.get_paginated_response(pagination1)
#
#         return response2
#

