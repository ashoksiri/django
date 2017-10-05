import rest_framework_mongoengine.viewsets as mongoviewsets
from socialanalytics.serializers import YoutubeSerializer,StandardResultsSetPagination
from socialanalytics.utils import refresh_data
from django.core.cache import cache
from socialanalytics.utils import filtermodels
from datetime import date , datetime,timedelta
from dateutil import parser
from socialanalytics.models import Video
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from socialanalytics.utils.wordcloud import getWordCloud
from mongoengine.queryset.visitor import Q
from socialanalytics.utils.filtermodels import getdaterange

current_date = int(datetime.now().date().strftime("%S"))

class YoutubeLiveData(mongoviewsets.GenericViewSet):

    """
        This Will Retrive the Live videos from The Twitter Api Matched with Search Keyword

    """
    def list(self,request,searchKey):
       data = []
       if searchKey and len(searchKey) > 0:
           data = cache.get(searchKey + "_youtube", None)
           data = data if data else refresh_data.load_key_data(searchKey, "youtube")
           return Response(data)
       else:
           return Response(data)

    def get_queryset(self):
        return self.list(self.request)

class YoutubeHistoryData(mongoviewsets.ReadOnlyModelViewSet):

    """
        This View will return Youtube videos from Database matched with searchKey and b/w the give date range.

    """
    serializer_class = YoutubeSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'videoid'

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        videos = []

        if searchKey is not None and len(searchKey) > 0:
            from_date = self.request.GET.get('from_date', '')
            to_date   = self.request.GET.get('to_date', '')
            subkey    = self.request.GET.get('subkey', None)
            sentiment = self.request.GET.get('sentiment', None)
            daterange = getdaterange(from_date,to_date)
            youtube_key = searchKey + '_' + str(subkey) + '_' + str(from_date) + '_' + str(to_date) + '_youtubedata'

            if (sentiment is not None and sentiment != '') and (subkey is None or subkey == ''):
                videos = Video.objects(Q(polarity__key=sentiment) &
                                     Q(searchKey=searchKey) &
                                     Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                     Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by(
                    '-snippet.publishedAt')
                return videos

            if (subkey is not None and subkey != '') and (sentiment is not None and sentiment != ''):

                videos = Video.objects(Q(polarity__key=sentiment) &
                                       Q(snippet__descriptionParsed__icontains=subkey)&
                                       Q(searchKey=searchKey) &
                                       Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                       Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by(
                    '-snippet.publishedAt')
                return videos



            if subkey is not None and subkey != '':
                videos = Video.objects(Q(snippet__descriptionParsed__icontains=subkey) &
                                       Q(searchKey=searchKey) &
                                       Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                       Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by(
                    '-snippet.publishedAt')
                return videos
            else:
                videos = Video.objects(Q(searchKey=searchKey) &
                                       Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                       Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by(
                    '-snippet.publishedAt')

            if len(videos) == 0:
                videos = cache.get(youtube_key)
                if videos:
                    return videos
                videos = refresh_data.load_key_data(searchKey, "youtube")
                videos = filtermodels.filterwithsubkey(data=videos, subkey=subkey, source="youtube", from_date=from_date,
                                                     to_date=to_date)
                cache.set(youtube_key, videos)
                return videos
            else:
                return videos
        else:
            return videos

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%S")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(YoutubeHistoryData, self).dispatch(request, *args, **kwargs)

class YoutubeAggregation(mongoviewsets.GenericViewSet):
    """

        This View will return the total count and date wise frequency of tweets from the database matched with the searchKey and b/w the date range give.

    """

    def list(self,request,searchKey):
        if searchKey is not None and len(searchKey) > 0:
            from_date = request.GET.get('from_date', '')
            to_date = request.GET.get('to_date', '')
            subkey = self.request.GET.get('subkey', None)
            if subkey is not None and subkey != '':
                pipeline = filtermodels.getpipelinewithaggregation("youtube",searchKey,from_date,to_date)
                pipeline[0].get('$match').__setitem__('description_parsed', {'$regex': r'\b{}\b'.format(subkey)})
            else :
                pipeline = filtermodels.getpipelinewithaggregation("youtube", searchKey, from_date, to_date)
            videos = [v for v in Video.objects.aggregate(*pipeline,allowDiskUse=True)]
            totalcount = [r.get('count') for r in videos]
            return Response({"totalcount": sum(totalcount), "data": videos})
        else:
            return Response({"totalcount": 0, "data": []})

    def get_queryset(self):
        return self.list(self.request)

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(YoutubeAggregation, self).dispatch(request, *args, **kwargs)

class GetStatistcs(mongoviewsets.GenericViewSet):

    def list(self,request,searchKey):
        return self.get_queryset()

    def get_queryset(self):
        searchKey   = self.kwargs['searchKey']
        from_date   = self.request.GET.get('from_date', '')
        to_date     = self.request.GET.get('to_date', '')
        subkey      = self.request.GET.get('subkey', None)
        pipelines   = filtermodels.getYoutubePiplines(searchKey=searchKey,from_date=from_date,to_date=to_date,subkey=subkey)
        statisitcs  = list(Video.objects.aggregate(*pipelines.get('statisitcs')))
        categorywise = list(Video.objects.aggregate(*pipelines.get('categorywise')))
        commentSentiment = list(Video.objects.aggregate(*pipelines.get('commentSentiment')))
        videosSentiment = list(Video.objects.aggregate(*pipelines.get('videosSentiment')))
        channelwise  =    list(Video.objects.aggregate(*pipelines.get('channelwise')))
        counts = list(Video.objects.aggregate(*pipelines.get('counts')))
        videoScores = list(Video.objects.aggregate(*pipelines.get('videoScores')))
        description = ' '.join(list(Video.objects.aggregate(*pipelines.get('description')))[0].get('description'))
        wordcloud = getWordCloud(description)
        return Response({'statisitcs':statisitcs,
                         'categorywise':categorywise,
                         'videosSentiment':videosSentiment,
                         'commentSentiment':commentSentiment,
                         'channelwise':channelwise,
                         'counts':counts,
                         'videoScores':videoScores,
                         'wordcloud':wordcloud
                         })

class GetVideosByCategory(mongoviewsets.ReadOnlyModelViewSet):

    serializer_class = YoutubeSerializer
    def get_queryset(self):
        searchKey  = self.kwargs['searchKey']
        categoryid = self.kwargs['categoryId']
        from_date  = self.request.GET.get('from_date',None)
        to_date    = self.request.GET.get('to_date')
        daterange = getdaterange(from_date=from_date, to_date=to_date)
        data = Video.objects(Q(snippet__categoryId__exact=categoryid) &
                             Q(searchKey=searchKey) &
                             Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                             Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')
        return data

class GetVideosByPolarity(mongoviewsets.ReadOnlyModelViewSet):

    serializer_class = YoutubeSerializer
    def get_queryset(self):
        searchKey  = self.kwargs['searchKey']
        start = self.request.GET.get('start',None)
        end   = self.request.GET.get('end',None)
        eq    = self.request.GET.get('eq',None)
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        daterange = getdaterange(from_date=from_date,to_date=to_date)
        if eq is not None and eq!= '':
            data = Video.objects(Q(polarity__value=float(eq)) &
                                 Q(searchKey=searchKey) &
                                 Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                 Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')
        else:
            data = Video.objects(Q(polarity__value__gt=float(start)) &
                                 Q(polarity__value__lt=float(end)) &
                                 Q(searchKey=searchKey) &
                                 Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                                 Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')
        return data

class GetVideosByChannel(mongoviewsets.ReadOnlyModelViewSet):

    serializer_class = YoutubeSerializer

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        channelId = self.kwargs['channelId']
        from_date = self.request.GET.get('from_date')
        to_date   = self.request.GET.get('to_date')
        daterange = getdaterange(from_date=from_date, to_date=to_date)
        data = Video.objects(Q(channelId=channelId) &
                             Q(searchKey=searchKey) &
                             Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                             Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')

        return data

class GetVideoBySentiment(mongoviewsets.ReadOnlyModelViewSet):

    serializer_class = YoutubeSerializer

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        sentiment = self.kwargs['sentiment']
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        daterange = getdaterange(from_date=from_date, to_date=to_date)
        data = Video.objects(Q(polarity__key__exact=sentiment) &
                             Q(searchKey=searchKey) &
                             Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                             Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')

        return data

class GetVideoBySubKey(mongoviewsets.ReadOnlyModelViewSet):
    serializer_class = YoutubeSerializer

    def get_queryset(self):
        searchKey = self.kwargs['searchKey']
        subKey = self.kwargs['subkey']
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        daterange = getdaterange(from_date=from_date, to_date=to_date)
        data = Video.objects(Q(snippet__descriptionParsed__icontains=subKey) &
                             Q(searchKey=searchKey) &
                             Q(snippet__publishedAt__gte=daterange.get('from_date')) &
                             Q(snippet__publishedAt__lte=daterange.get('to_date'))).order_by('-snippet.publishedAt')

        return data

class GetVideoStats(mongoviewsets.GenericViewSet):

    def getSentiments(self,comments):
        sentiment = {'positive':0,'negative':0,'neutral':0}
        for comment in comments:
            if comment.polarity.key == 'positive':
                sentiment['positive'] = sentiment['positive']+1
            if comment.polarity.key == 'negative':
                sentiment['negative'] = sentiment['negative']+1
            if comment.polarity.key == 'positive':
                sentiment['neutral'] = sentiment['neutral']+1
        return sentiment

    def list(self,request,videoId):
        return self.get_queryset()

    def get_queryset(self):
        videoId = self.kwargs['videoId']
        video = Video.objects(videoId=videoId)[0]
        description = ' '.join([comment.snippet.topLevelComment.snippet.textOriginalParsed for comment in video.comments
                       if comment.snippet.topLevelComment.snippet.textOriginalParsed is not None ])
        wordcloud  = getWordCloud(description)
        sentiment  = self.getSentiments(video.comments)
        data = YoutubeSerializer(video).data
        data['wordcloud'] = wordcloud
        data['sentiment'] = sentiment
        return Response(data)