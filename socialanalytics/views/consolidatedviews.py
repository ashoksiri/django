# -*- coding: utf-8 -*-

import rest_framework_mongoengine.viewsets as mongoviewsets
from socialanalytics.models import Facebook, Video,News,Tweet
from dateutil.parser import parse
from datetime import date,datetime
from socialanalytics.utils import refresh_data, filtermodels as filter
from socialanalytics.models import Tweet
from django.http import JsonResponse
from rest_framework.response import Response
from socialanalytics.serializers import StandardResultsSetPagination
from rest_framework import status
from dateutil import parser
from socialanalytics.utils import filtermodels

current_date = int(datetime.now().date().strftime("%S"))

"""
    Consolidated Data from 4 channels 
    
    Picking 10 Recent Records from each channel  b/w the given date Range.
    
    And finding cumulative poplarity for 4 channels sending it as Responce
    
    
    Sample Response : 
    
    {
        "results":[
            {
                "facebook" : {},
                "twitter"  : {},
                "youtube"  : {},
                "news"     : {},
                "polarity" : {} #cummulative polarity of the above 4 objects.
            }
        ]
            
    }

"""


def consolidated(request,searchKey):

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    subkey = request.GET.get('subkey', None)
    subkey = None if subkey == '' else subkey

    def arrangeData(fb_data, tw_data, yt_data, nw_data):

        consolidatedList = []

        """
            Creating a safe List of objects.
        """

        polarity = {'positive': 0, 'negative': 0, 'neutral': 0}

        for i in range(0, 10):
            fb = filtermodels.safe_list_get(fb_data, i, None)
            nw = filtermodels.safe_list_get(nw_data, i, None)
            yu = filtermodels.safe_list_get(yt_data, i, None)
            tw = filtermodels.safe_list_get(tw_data, i, None)

            data = filter.aggregatepolarity(fb, tw, yu, nw)
            polarity['positive'] = polarity['positive'] + data['positive']
            polarity['negative'] = polarity['negative'] + data['negative']
            polarity['neutral'] = polarity['neutral'] + data['neutral']

            consolidatedList.append({
                "facebook": fb,
                "news": nw,
                "youtube": yu,
                "twitter": tw,
            })
        return consolidatedList, polarity

    if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
        content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)

    if searchKey not in KeyWords.objects().distinct('keyword'):
        data = refresh_data.load_all_dala(searchKey)
        facebook = filtermodels.filterwithsubkey(data.get('facebook'), source="facebook", subkey=subkey, from_date=from_date,to_date=to_date)
        twitter  = filtermodels.filterwithsubkey(data.get('twitter'), source="twitter", subkey=subkey, from_date=from_date,
                                                to_date=to_date)
        youtube  = filtermodels.filterwithsubkey(data=data.get('youtube'), source="youtube", subkey=subkey, from_date=from_date,
                                                to_date=to_date)
        news     = filtermodels.filterwithsubkey(data=data.get('news'), subkey=subkey, source="news", from_date=from_date,
                                             to_date=to_date)
        consolidateddata, polarity = arrangeData(fb_data=facebook, tw_data=twitter, nw_data=news, yt_data=youtube)

        keywords = KeyWords(id=KeyWords.objects().count()+1,keyword=searchKey)
        keywords.save()

        return JsonResponse({'results': consolidateddata, 'polarity': polarity}, safe=False)
    # if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) == current_date \
    #         or searchKey not in Tweet.objects.distinct('searchKey'):
    #     refresh_data.load_all_dala(searchKey)



    """
        Getting the Recent 10 Records from Database from the give date Range
    """

    if subkey:

        facebookfilter = filter.getpipeline("facebook", searchKey, from_date, to_date, 10)
        facebookfilter[0].get('$match').__setitem__('message_parsed',
                                                    {'$regex': r'\b{}\b'.format(subkey)})  # ['message_parsed']
        twitterfilter = filter.getpipeline("twitter", searchKey, from_date, to_date, 10)
        twitterfilter[0].get('$match').__setitem__('text_parsed', {'$regex': r'\b{}\b'.format(subkey)})
        youtubefilter = filter.getpipeline("youtube", searchKey, from_date, to_date, 10)
        youtubefilter[0].get('$match').__setitem__('videodescription_parsed', {'$regex': r'\b{}\b'.format(subkey)})
        newsfilter = filter.getpipeline("news", searchKey, from_date, to_date, 10)
        newsfilter[0].get('$match').__setitem__('description_parsed', {'$regex': r'\b{}\b'.format(subkey)})

        facebook = [f for f in Facebook.objects.aggregate(*facebookfilter, allowDiskUse=True)]
        news = [n for n in News.objects.aggregate(*newsfilter, allowDiskUse=True)]
        youtube = [v for v in Video.objects.aggregate(*youtubefilter, allowDiskUse=True)]
        twitter = [t for t in Tweet.objects.aggregate(*twitterfilter, allowDiskUse=True)]

    else:
        facebookfilter = filter.getpipeline("facebook", searchKey, from_date, to_date, 10)
        facebook = [f for f in Facebook.objects.aggregate(*facebookfilter, allowDiskUse=True)]

        newsfilter = filter.getpipeline("news", searchKey, from_date, to_date, 10)
        news = [n for n in News.objects.aggregate(*newsfilter, allowDiskUse=True)]

        youtubefilter = filter.getpipeline("youtube", searchKey, from_date, to_date, 10)
        youtube = [v for v in Video.objects.aggregate(*youtubefilter, allowDiskUse=True)]

        twitterfilter = filter.getpipeline("twitter", searchKey, from_date, to_date, 10)
        twitter = [t for t in Tweet.objects.aggregate(*twitterfilter, allowDiskUse=True)]

    if len(facebook) == 0:
        fb_data = refresh_data.load_key_data(searchKey, "facebook")
        facebook = filtermodels.filterwithsubkey(fb_data, source="facebook", subkey=subkey, from_date=from_date,
                                                 to_date=to_date)
    if len(twitter) == 0:
        tweets = refresh_data.load_key_data(searchKey, "twitter")
        twitter = filtermodels.filterwithsubkey(tweets, source="twitter", subkey=subkey, from_date=from_date,
                                                to_date=to_date)
    if len(youtube) == 0:
        videos = refresh_data.load_key_data(searchKey, 'youtube')
        youtube = filtermodels.filterwithsubkey(data=videos, source="youtube", subkey=subkey, from_date=from_date,
                                                to_date=to_date)
    if len(news) == 0:
        newss = refresh_data.load_key_data(searchKey, "news")
        news = filtermodels.filterwithsubkey(data=newss, subkey=subkey, source="news", from_date=from_date,
                                             to_date=to_date)


    consolidateddata , polarity = arrangeData(fb_data=facebook,tw_data=twitter,nw_data=news,yt_data=youtube)

    return JsonResponse({'results': consolidateddata, 'polarity': polarity},safe=False)

class GetSentiment(mongoviewsets.GenericViewSet):

    def list(self,request,searchKey):
        if searchKey is None or searchKey is '':
            return Response([])

        from_date = self.request.GET.get('from_date', '')
        to_date   = self.request.GET.get('to_date', '')
        subkey = request.GET.get('subkey',None)
        subkey = None if subkey == '' else subkey

        if subkey:
            npipeline = filter.sentimentPipeline(searchKey=searchKey, from_date=from_date, to_date=to_date)
            npipeline[0].get('$match').__setitem__('description_parsed', {'$regex': r'\b{}\b'.format(subkey)})

            fpipeline = filter.sentimentPipeline(searchKey=searchKey, from_date=from_date, to_date=to_date)
            fpipeline[0].get('$match').__setitem__('message_parsed', {'$regex': r'\b{}\b'.format(subkey)})

            ypipeline = filter.sentimentPipeline(searchKey=searchKey, from_date=from_date, to_date=to_date)
            ypipeline[0].get('$match').__setitem__('videodescription_parsed', {'$regex': r'\b{}\b'.format(subkey)})

            tpipeline = filter.sentimentPipeline(searchKey=searchKey, from_date=from_date, to_date=to_date)
            tpipeline[0].get('$match').__setitem__('text_parsed', {'$regex': r'\b{}\b'.format(subkey)})

            tcounts = [t for t in Tweet.objects.aggregate(*tpipeline)]
            fcounts = [t for t in Facebook.objects.aggregate(*fpipeline)]
            ncounts = [t for t in News.objects.aggregate(*npipeline)]
            vcounts = [t for t in Video.objects.aggregate(*ypipeline)]


        else:
            pipeline = filter.sentimentPipeline(searchKey=searchKey,from_date=from_date,to_date=to_date)
            tcounts = [t for t in Tweet.objects.aggregate(*pipeline)]
            fcounts = [t for t in Facebook.objects.aggregate(*pipeline)]
            ncounts = [t for t in News.objects.aggregate(*pipeline)]
            vcounts = [t for t in Video.objects.aggregate(*pipeline)]


        polarity = {'positive':0.0,'negative':0.0,'neutral':0.0}

        for i in range(0, len(tcounts)):
            if  tcounts[i].get('key') == 'positive':
                polarity['positive']= polarity['positive'] + tcounts[i].get('count')
            if  tcounts[i].get('key') == 'negative':
                polarity['negative']= polarity['negative'] + tcounts[i].get('count')
            if  tcounts[i].get('key') == 'neutral':
                polarity['neutral']= polarity['neutral'] + tcounts[i].get('count')
        for i in range(0, len(fcounts)):
            if  fcounts[i].get('key') == 'positive':
                polarity['positive']= polarity['positive'] + fcounts[i].get('count')
            if  fcounts[i].get('key') == 'negative':
                polarity['negative']= polarity['negative'] + fcounts[i].get('count')
            if  fcounts[i].get('key') == 'neutral':
                polarity['neutral']= polarity['neutral'] + fcounts[i].get('count')
        for i in range(0, len(vcounts)):
            if  vcounts[i].get('key') == 'positive':
                polarity['positive']= polarity['positive'] + vcounts[i].get('count')
            if  vcounts[i].get('key') == 'negative':
                polarity['negative']= polarity['negative'] + vcounts[i].get('count')
            if  vcounts[i].get('key') == 'neutral':
                polarity['neutral']= polarity['neutral'] + vcounts[i].get('count')
        for i in range(0,len(ncounts)):
            if  ncounts[i].get('key') == 'positive':
                polarity['positive']= polarity['positive'] + ncounts[i].get('count')
            if  ncounts[i].get('key') == 'negative':
                polarity['negative']= polarity['negative'] + ncounts[i].get('count')
            if  ncounts[i].get('key') == 'neutral':
                polarity['neutral']= polarity['neutral'] + ncounts[i].get('count')

        return Response(polarity)

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
            return super(GetSentiment, self).dispatch(request, *args, **kwargs)

class searchFeed(mongoviewsets.GenericViewSet):
    def list(self,request,searchKey,subKey):
        if searchKey is None or searchKey is '':
            return Response([])

        from_date = self.request.GET.get('from_date', '')
        to_date = self.request.GET.get('to_date', '')

        """
            Getting the Recent 10 Records from Database from the give date Range
        """
        facebookfilter = filter.getpipeline("facebook", searchKey, from_date, to_date, 5)
        facebookfilter[0].get('$match').__setitem__('message_parsed',{'$regex': r'\b{}\b'.format(subKey)}) #['message_parsed']
        twitterfilter = filter.getpipeline("twitter", searchKey, from_date, to_date, 5)
        twitterfilter[0].get('$match').__setitem__('text_parsed', {'$regex': r'\b{}\b'.format(subKey)})
        youtubefilter = filter.getpipeline("youtube", searchKey, from_date, to_date, 5)
        youtubefilter[0].get('$match').__setitem__('videodescription_parsed', {'$regex': r'\b{}\b'.format(subKey)})
        newsfilter = filter.getpipeline("news", searchKey, from_date, to_date, 5)
        newsfilter[0].get('$match').__setitem__('description_parsed', {'$regex': r'\b{}\b'.format(subKey)})

        facebook = [f for f in Facebook.objects.aggregate(*facebookfilter,allowDiskUse=True)]
        news     = [n for n in News.objects.aggregate(*newsfilter,allowDiskUse=True)]
        youtube  = [v for v in Video.objects.aggregate(*youtubefilter,allowDiskUse=True)]
        twitter  = [t for t in Tweet.objects.aggregate(*twitterfilter,allowDiskUse=True)]
        consolidatedList = []

        """
            Creating a safe List of objects.
        """

        polarity = {'positive': 0, 'negative': 0, 'neutral': 0}

        for i in range(0, 5):
            fb = self.safe_list_get(facebook, i, None)
            nw = self.safe_list_get(news, i, None)
            yu = self.safe_list_get(youtube, i, None)
            tw = self.safe_list_get(twitter, i, None)

            data = filter.aggregatepolarity(fb, tw, yu, nw)
            polarity['positive'] = polarity['positive'] + data['positive']
            polarity['negative'] = polarity['negative'] + data['negative']
            polarity['neutral'] = polarity['neutral'] + data['neutral']

            consolidatedList.append({
                "facebook": fb,
                "news": nw,
                "youtube": yu,
                "twitter": tw,
            })
        return Response({'results': consolidatedList, 'polarity': polarity})

    def safe_list_get(self, l, idx, default):
        try:
            return l[idx]
        except IndexError:
            return default


    def get_queryset(self):
        return self.list(request=self.request,searchKey=self.kwargs['searchKey'],subKey= self.kwargs['subKey'])

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(searchFeed, self).dispatch(request, *args, **kwargs)

class searchFeedWithSentiment(mongoviewsets.GenericViewSet):
    def list(self,request,searchKey,sentiment):
        if searchKey is None or searchKey is '':
            return Response([])

        from_date = self.request.GET.get('from_date', '')
        to_date = self.request.GET.get('to_date', '')

        """
            Getting the Recent 10 Records from Database from the give date Range
        """
        facebookfilter = filter.getpipeline("facebook", searchKey, from_date, to_date, 10)
        facebookfilter[0].get('$match').__setitem__('polarity.key',{'$eq': sentiment}) #['message_parsed']
        twitterfilter = filter.getpipeline("twitter", searchKey, from_date, to_date, 10)
        twitterfilter[0].get('$match').__setitem__('polarity.key',{'$eq': sentiment})
        youtubefilter = filter.getpipeline("youtube", searchKey, from_date, to_date, 10)
        youtubefilter[0].get('$match').__setitem__('polarity.key',{'$eq': sentiment})
        newsfilter = filter.getpipeline("news", searchKey, from_date, to_date, 10)
        newsfilter[0].get('$match').__setitem__('polarity.key',{'$eq': sentiment})

        facebook = [f for f in Facebook.objects.aggregate(*facebookfilter,allowDiskUse=True)]
        news     = [n for n in News.objects.aggregate(*newsfilter,allowDiskUse=True)]
        youtube  = [v for v in Video.objects.aggregate(*youtubefilter,allowDiskUse=True)]
        twitter  = [t for t in Tweet.objects.aggregate(*twitterfilter,allowDiskUse=True)]

        consolidatedList = []

        """
            Creating a safe List of objects.
        """

        polarity = {'positive': 0, 'negative': 0, 'neutral': 0}

        for i in range(0, 10):
            fb = self.safe_list_get(facebook, i, None)
            nw = self.safe_list_get(news, i, None)
            yu = self.safe_list_get(youtube, i, None)
            tw = self.safe_list_get(twitter, i, None)

            data = filter.aggregatepolarity(fb, tw, yu, nw)
            polarity['positive'] = polarity['positive'] + data['positive']
            polarity['negative'] = polarity['negative'] + data['negative']
            polarity['neutral'] = polarity['neutral'] + data['neutral']

            consolidatedList.append({
                "facebook": fb,
                "news": nw,
                "youtube": yu,
                "twitter": tw,
            })
        return Response({'results': consolidatedList, 'polarity': polarity})

    def safe_list_get(self, l, idx, default):
        try:
            return l[idx]
        except IndexError:
            return default

    def get_queryset(self):
        return self.list(request=self.request,searchKey=self.kwargs['searchKey'],sentiment= self.kwargs['sentiment'])

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        to_date = request.GET.get('to_date', '')
        if to_date != '' and int(parser.parse(to_date).date().strftime("%s")) > current_date:
            content = {'error': 'GraterThan current_date not Allowed', 'status_code': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            return super(searchFeedWithSentiment, self).dispatch(request, *args, **kwargs)
