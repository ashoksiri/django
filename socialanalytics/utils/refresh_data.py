
from django.core.cache import cache
import time
from datetime import datetime
from socialanalytics.serializers import *
import multiprocessing
from facebookUtils import FetchFacebookData
from twitterUtils import TwitterUtils
from youtubeUtils import getvideos
import GoogleNewsRSS as news_utils
from mongoengine.queryset.visitor import Q
from multiprocessing import Manager,Process
import rssutils

keys = set()
fb = FetchFacebookData()
twitter_utils   =  TwitterUtils()


def run():
    while True:
        print("Refreshing Posts")
        refresh()
        time.sleep(5)

def create_documents(key, data,type):
    print "Loding Data to DB........"

    if type == 'facebook':
        for d in data:
            record = Facebook.objects(Q(searchKey=key) & Q(postid=d['postid']))
            if len(record) > 0:
                record = record[0]
                comments = record.comments
                if len(comments) > 0:
                    tempcomments = [ comment.__dict__() for comment in comments]
                    commentids   = [id.get('commentid') for id in tempcomments]
                    livecomments = [x for x in d['comments'] if x['commentid'] not in commentids]
                    totlacomments = tempcomments + livecomments
                    d['comments'] = totlacomments

                serializer = FacebookSerializer(instance=record,data=d)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print serializer.errors
            else:
                d['searchKey'] = key
                serializer = FacebookSerializer(data=d)
                serializer.is_valid(raise_exception=True)
                serializer.save()
    elif type == "youtube" :
        for d in data:

            record = Video.objects(Q(searchKey=key)& Q(videoId = d['videoId']))

            if len(record) > 0:
                record = record[0]
                comments = record.comments
                if comments is not None and len(comments) > 0:
                    tempcomments = [comment.__dict__() for comment in comments]
                    commentids = [id.get('commentId') for id in tempcomments]
                    livecomments = [x for x in d['comments'] if x['commentId'] not in commentids]
                    totlacomments = tempcomments + livecomments
                    d['comments'] = totlacomments
                serializer = YoutubeSerializer(instance=record,data=d)
                serializer.is_valid(raise_exception=False)
                serializer.save()
            else:
                d['searchKey'] = key
                serializer = YoutubeSerializer(data=d)
                serializer.is_valid(raise_exception=False)
                serializer.save()
    elif type == "twitter":
        for d in data:

            record = Tweet.objects(Q(searchKey=key) & Q(tweetid=d['tweetid']))
            if len(record) > 0:
                record = record[0]
                serializer = TwitterSerializer(instance=record, data=d)
                if not serializer.is_valid():
                    print serializer.errors
                serializer.save()
            else:
                d['searchKey'] = key
                serializer = TwitterSerializer(data=d)
                serializer.is_valid(raise_exception=False)
                serializer.save()

    elif type == "news":
        for d in data:
            record = News.objects(Q(searchKey=key) & Q(newsid=d['newsid']))
            if len(record) > 0:
                record = record[0]
                serializer = NewsSerializer(instance=record, data=d)
                serializer.is_valid(raise_exception=False)
                serializer.save()
            else:
                d['searchKey'] = key
                serializer = NewsSerializer(data=d)
                serializer.is_valid(raise_exception=False)
                serializer.save()

            # self.perform_create(serializer2)


def load_key_data(key,type):

    print("calling load key data "+type+' '+datetime.now().__str__())

    if type   == "facebook":
        data   = fb.scrapeFacebookPageFeedStatus(q=key)
    elif type == "youtube":
         data  = getvideos(q=key)
    elif type == 'twitter' :
        data   = twitter_utils.getTweetswithAll(searchKey=key)
    elif type == 'news' :
         data  = news_utils.getNews(key)

    keys.add(key+"_"+type)
    if len(data) > 0:
        cache.set(key+"_"+type, data)
    p = multiprocessing.Process(target=create_documents,args=(key,data,type))
    p.start()
    print "Data Returned for",type
    return data

def worker(L, num, q, ):
    if num == 1:
        L.append({'facebook':load_key_data(key=q, type='facebook')})
    if num == 2:
        L.append({'twitter':load_key_data(key=q, type='twitter')})
    if num == 3:
        L.append({'youtube':load_key_data(key=q, type='youtube')})
    if num == 4:
        L.append({'news':load_key_data(key=q, type='news')})

def load_all_dala(key):

    with Manager() as manager:
        L = manager.list()
        jobs = []
        for i in range(5):
            p = Process(target=worker, args=(L, i, key,))
            p.start()
            jobs.append(p)
        for p in jobs:
            p.join()

        data = {}
        for i in L :
            for k,v in i.items():
                data[k] = v
        return data

def refresh():
    # Read Search Terms From Cache
    # Make Request for each Term.
    # Grab The Response and update the Cache with new response.

    for term in keys:
        load_key_data(term)
        print("Loaded posts for: " + term)

