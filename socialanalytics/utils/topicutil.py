
from socialanalytics.models import Tweet,Facebook,News,Video
from socialanalytics.utils import filtermodels as filter
from datetime import datetime,timedelta
from socialanalytics.utils import filtermodels
import re,time,json,requests,mongoengine
from multiprocessing import Process, Manager

#db = mongoengine.connect(db='db_apsma_bak')
regex = "(@[A-Za-z0-9]+)|([^0-9A-Za-z\'\"\,\. \t])|(\w+:\/\/\S+)|(RT)"
db = mongoengine.connect(db='db_apsma_bak',host='10.1.4.57')

cleanDict = {}

def cleanMap(data,type):

        if type == 'T':
            text  = data.get('text_parsed') if data.get('text_parsed') else ''
            return {
                ' '.join(re.sub(regex, " ", text).split()):
                    {'type':'T','id':data.get('tweetid'),'polarity':data.get('polarity'),'created_time':data.get('created_at'),'object':data}}
        if type == 'F':
            message = data.get('message_parsed') if data.get('message_parsed') else ''
            return {
                ' '.join(re.sub(regex, " ", message).split()):
                    {'type':'F','id':data.get('postid'),'polarity':data.get('polarity'),'created_time':data.get('created_time'),'object':data}}
        if type == 'Y':
            videodescription = data.get('videodescription_parsed') if data.get('videodescription_parsed') else ''
            return {
                ' '.join(re.sub(regex, " ", videodescription).split()):
                    {'type':'Y','id':data.get('videoid'),'polarity':data.get('polarity'),'created_time':data.get('publishedat'),'object':data}}
        if type == 'N':
            description = data.get('description_parsed') if data.get('description_parsed') else ''
            return {
                ' '.join(re.sub(regex, " ", description).split()):
                    {'type':'N','id':data.get('newsid'),'polarity':data.get('polarity'),'created_time':data.get('created_at'),'object':data}}


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def worker(L, num, q, from_date, to_date):
    if num == 1:
        tpipe = filter.getpipeline("twitter", q, from_date, to_date, 50)
        data = [cleanMap(data=t, type='T') for t in Tweet.objects.aggregate(*tpipe)]
        L.append(data)

    if num == 2:
        fpipe = filter.getpipeline("facebook", q, from_date, to_date, 50)
        data = [cleanMap(data=t, type='F') for t in Facebook.objects.aggregate(*fpipe)]
        L.append(data)

    if num == 3:
        ypipe = filter.getpipeline("youtube", q, from_date, to_date, 50)
        data = [cleanMap(data=t, type='Y') for t in Video.objects.aggregate(*ypipe)]
        L.append(data)

    if num == 4:
        npipe = filter.getpipeline("news", q, from_date, to_date, 50)
        data = [cleanMap(data=t, type='N') for t in News.objects.aggregate(*npipe)]
        L.append(data)


def getdescriptions(searchKey,from_date=None,to_date=None):
    with Manager() as manager:
        L = manager.list()
        jobs = []
        for i in range(5):
            p = Process(target=worker, args=(L,i,searchKey,from_date,to_date,))
            p.start ()
            jobs.append(p)
        for p in jobs:
            p.join()
        data = [val for sublist in L for val in sublist]
        return data;



def gettopics(searchKey,from_date=None,to_date=None):

    cleanDict = {}
    with Manager() as manager:
        L = manager.list()
        jobs = []
        for i in range(5):
            p = Process(target=worker, args=(L,i,searchKey,from_date,to_date,))
            p.start ()
            jobs.append(p)
        for p in jobs:
            p.join()


        data = [val for sublist in L for val in sublist]

        for x in data:
            if x.keys()[0] not in cleanDict.keys():
                cleanDict[x.keys()[0]] = x.values()[0]


        text = '\n'.join([ k for k,v in cleanDict.items()])



        apiurl          = "http://api.meaningcloud.com/clustering-1.1"
        payload         = "key=b122b13a68435ad7d316440ef2b62345&lang=en&txt="+text
        headers         = {'content-type': 'application/x-www-form-urlencoded'}
        response        = requests.request("POST", apiurl, data=payload, headers=headers)
        topicsjson      = json.loads(response.text)
        cluster_json    = topicsjson.get('cluster_list', {})

        sentencetopicList = []

        for cj in cluster_json:
            sentencetopic   = {}
            polarityValList = []
            descjsonList    = []
            datejsonList    = []
            finalcountlist  = []
            alldateslist    = []
            finaldatelist   = []

            for cjd in cj['document_list']:

                doc = cj['document_list'][cjd]
                object_id   = cleanDict.get(doc).get('id')
                object_type = cleanDict.get(doc).get('type')
                polarity    = cleanDict.get(doc).get('polarity')
                polarityValList.append(float(polarity.get('value')))

                sentencetopic['topic'] = cj['title']

                sentence_date = cleanDict.get(doc).get('created_time')

                # if object_id !='':
                #
                #     if(object_type == 'T'):
                #         sentence_date = datetime.date(Tweet.objects(tweetid=object_id)[0].created_at)
                #     if (object_type == 'F'):
                #         sentence_date = datetime.date(Facebook.objects(postid=object_id)[0].created_time)
                #     if (object_type == 'N'):
                #         sentence_date = datetime.date(News.objects(newsid=object_id)[0].created_at)
                #     if (object_type == 'Y'):
                #         sentence_date = datetime.date(Video.objects(videoid=object_id)[0].publishedat)


                #descjsonList.append({'id':object_id,'sentence_date':str(sentence_date),'text':doc,'type':object_type})
                descjsonList.append(
                    {'data': cleanDict.get(doc).get('object') , 'type': object_type})

                datejsonList.append(str(sentence_date.date()))


            date_data       = filtermodels.getdaterange(from_date, to_date)
            fr_date         = date_data.get('from_date').date()
            t_date          = date_data.get('to_date').date()
            daterangelist   = perdelta(fr_date, t_date, timedelta(days=1))

            for result1 in daterangelist:

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
                sentencetopic['value'] = float(0.0)
            else:
                sentencetopic['key'] = "Negative"
                sentencetopic['value'] = maxpolval

            sentencetopicList.append(sentencetopic)
        result = sentencetopicList
        #print result
        return result

if __name__ == '__main__':
    starttime = time.time()

    gettopics(searchKey='narendramodi',from_date='2017-08-01',to_date='2017-08-29')

    print starttime - time.time() , "Seconds"