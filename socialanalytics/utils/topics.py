import requests,re,sys,json
from socialanalytics.models import *
import filtermodels
import mongoengine
from sentimentUtils import SentimentUtils
from multiprocessing import Process, Manager
from django.core.cache import cache
from datetime import date, datetime, timedelta
import time

sutils = SentimentUtils()

apiurl = "http://api.meaningcloud.com/clustering-1.1"

db = mongoengine.connect(db='twitter',host='10.1.11.23')

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def worker(L, num,q,from_date,to_date):
    if num == 1:
        testdata = ""
        facebookpipeline = filtermodels.getpipeline(source='facebook', key=q, from_date=from_date, to_date=to_date,limit=50)
        #fb_data = [post.get('message') for post in Facebook.objects.aggregate(*facebookpipeline)]
        fb_data = [ post for post in Facebook.objects.aggregate(*facebookpipeline)]

        for post in fb_data:
            try:
                p =post['message']
            except:
                p=" "
            post_id = post['postid']
            source_lang = sutils.detect_language(p)
            try:
                if (str(source_lang) == "en"):
                    post1 = p
                else:
                    post1 = sutils.translate(p, from_lang=source_lang, to='en')
            except:
                post1 = p
            try:
                pn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", post1).split())
            except:
                pn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(post1)).split())

            post11 = " ".join(filter(lambda x: x[0] != '@', pn1.split()))
            #testdata = testdata + ".\n" + post1
            testdata = testdata +(post11 + " $" + post_id + "f$\n")

        L.append(testdata)

    if num == 2:
        testdata = ""
        twitterpipeline = filtermodels.getpipeline(source='twitter', key=q, from_date=from_date, to_date=to_date,limit=50)
        #tw_data = [tweet.get('text') for tweet in Tweet.objects.aggregate(*twitterpipeline)]
        tw_data = [tweet for tweet in Tweet.objects.aggregate(*twitterpipeline)]

        data = {}

        for tweet in tw_data:
            data[tweet['text']] = tweet['id_str']

        for t,id in data.items():
            #t = tweetlist['text']
            #tweet_id = tweetlist['tweetid']
            source_lang = sutils.detect_language(t)
            try:
                if (str(source_lang) == "en"):
                    tweet = t
                else:
                    tweet = sutils.translate(t, from_lang=source_lang, to='en')
            except:
                tweet = t
            try:
                tn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
            except:
                tn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())

            tweet1 = " ".join(filter(lambda x: x[0] != '@', tn1.split()))
            #testdata = testdata + ".\n" + tweet1
            testdata = testdata + (tweet1+" $" + str(id) + "t$\n")
        L.append(testdata)

    if num == 3:
        testdata = ""
        youtubepipeline = filtermodels.getpipeline(source='youtube', key=q, from_date=from_date, to_date=to_date,limit=50)
        #yu_data = [video.get('videodescription') for video in Video.objects.aggregate(*youtubepipeline)]
        yu_data = [video for video in Video.objects.aggregate(*youtubepipeline)]

        data = {}

        for ydata in yu_data:
            data[ydata['title']] = ydata['videoid']
        for k,v in data.items():
            # y = ydata['title']
            # y_id = ydata['videoid']
            source_lang = sutils.detect_language(k)

            try:
                if (str(source_lang) == "en"):
                    yt = k
                else:
                    yt = sutils.translate(k, from_lang=source_lang, to='en')
            except:
                yt = k
            try:
                yn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", yt).split())
            except:
                yn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(yt)).split())

            yy1 = " ".join(filter(lambda x: x[0] != '@', yn1.split()))
            #testdata = testdata + ".\n" + yy1
            testdata = testdata + (yy1 +" $" + str(v) + "y$\n")
        L.append(testdata)

    if num == 4:
        testdata = ""
        newspipeline = filtermodels.getpipeline(source='news', key=q, from_date=from_date, to_date=to_date,limit=50)
        #nw_data = [news.get('description') for news in News.objects.aggregate(*newspipeline)]
        nw_data = [news for news in News.objects.aggregate(*newspipeline)]
        for gdata in nw_data:
            g = gdata.get('description',None)
            g_id = gdata['newsid']
            source_lang = sutils.detect_language(g)

            try:
                if (str(source_lang) == "en"):
                    gt = g
                else:
                    gt = sutils.translate(g, from_lang=source_lang, to='en')
            except:
                gt = g
            try:
                gn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", gt).split())
            except:
                gn1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(gt)).split())

            gg1 = " ".join(filter(lambda x: x[0] != '@', gn1.split()))
            #testdata = testdata + ".\n" + gg1
            testdata = testdata + (gg1+" $" + g_id + "n$.\n")

        L.append(testdata)


def getTopics(q,from_date=None,to_date=None):

    print "Topics called ...."


    with Manager() as manager:
        L = manager.list()
        jobs = []
        for i in range(5):
            p = Process(target=worker, args=(L,i,q,from_date,to_date,))
            p.start ()
            jobs.append(p)
        for p in jobs:
            p.join()
        data = '\n'.join(L)



        #payload = "key=57078eaec1537818fd96584c21078d5a&lang=en&txt="+data
        payload = "key=b122b13a68435ad7d316440ef2b62345&lang=en&txt="+data
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", apiurl, data=payload, headers=headers)
        topicsjson =  json.loads(response.text)
        cluster_json = topicsjson.get('cluster_list', {})


        sentencetopicList = []

        for cj in cluster_json:
            sentencetopic = {}
            polarityValList = []
            descjsonList = []
            datejsonList = []
            source_type = ''
            finalcountlist = []
            alldateslist = []
            finaldatelist = []
            for cjd in cj['document_list']:

                doc = cj['document_list'][cjd]

                text_id = doc.partition('$')[-1].rpartition('$')[0][:-1]
                source_type = doc.partition('$')[-1].rpartition('$')[0][-1:]

                doc = doc[:doc.index('$')]

                try:
                    eachpolarity = sutils.get_sentiment(doc)
                    polarityValList.append(float(eachpolarity['value']))
                except:
                    polarityValList.append(float('0.0'))
                sentencetopic['topic'] = cj['title']

                sentence_date = ''
                if text_id !='':

                    pipeline = filtermodels.getDatewiseData(source=source_type,id=text_id)

                    if(source_type == 't'):

                        tweet = [t for t in Tweet.objects.aggregate(*pipeline)][0]
                        sentence_date = datetime.date(tweet.get('created_at'))
                    if (source_type == 'f'):

                        post = Facebook.objects(postid=text_id)[0]
                        sentence_date = datetime.date(post.created_time)
                    if (source_type == 'n'):

                        gnews = News.objects(newsid=text_id)[0]
                        sentence_date = datetime.date(gnews.created_at)
                    if (source_type == 'y'):

                        videos = Video.objects(videoid=text_id)[0]
                        sentence_date = datetime.date(videos.publishedat)

                    descjsonList.append({'id':text_id,'senten_date':str(sentence_date),'text':doc})
                    datejsonList.append(str(sentence_date))



            date_data = filtermodels.getdaterange(from_date, to_date)
            fr_date = date_data.get('from_date').date()
            t_date = date_data.get('to_date').date()
            daterangelist = perdelta(fr_date, t_date, timedelta(days=1))

            for result1 in daterangelist:
                #print result1
                alldateslist.append(str(result1))
                datecount = datejsonList.count(str(result1))
                finaldatelist.append(str(result1))
                finalcountlist.append(datecount)

            sentencetopic['trendsdate'] = finaldatelist
            sentencetopic['trendscount'] = finalcountlist
            sentencetopic['desc'] = descjsonList

            if (polarityValList == []):
                maxpolval = 0
            else:
                maxpolval = max(polarityValList)

            sentencetopic['score'] = cj['size']
            if maxpolval > 0:
                sentencetopic['key'] = "Positive"
                sentencetopic['value'] = maxpolval
            elif maxpolval == 0:
                sentencetopic['key'] = "Neutral"
                sentencetopic['value'] = "0.0"
            else:
                sentencetopic['key'] = "Negative"
                sentencetopic['value'] = maxpolval

            sentencetopicList.append(sentencetopic)
        result = sentencetopicList
        cache.set(q + '_topics', result)
        return result


if __name__ == '__main__':
    starttime = time.time()

    print getTopics(q='narendramodi',from_date='2017-08-01',to_date='2017-08-29')

    print starttime - time.time() , "Seconds"
    #print Facebook.objects.all()