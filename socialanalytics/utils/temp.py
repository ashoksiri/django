from multiprocessing import Process, Manager
from facebookUtils import FetchFacebookData
from youtubeUtils import YoutubeUtils
from twitterUtils import TwitterUtils
from GoogleNewsRSS import getNews
from collections import defaultdict
from dateutil.parser import parse

futils = FetchFacebookData()
yutils = YoutubeUtils()
tutils = TwitterUtils()

def worker(L, num,keyword):
    if num == 1:
        L.append(futils.scrapeFacebookPageFeedStatus(keyword))
    if num == 2:
        L.append(tutils.getTweets(keyword))
    if num == 3:
        L.append(yutils.getvideos(keyword))
    if num == 4:
        L.append(getNews(keyword))

def parsedata(data):

    tempdata = {}
    for i in range(0,len(data)):
        for k in data[i]:
            tempdata[k] = data[i][k]
    return tempdata

def getdata(keyword):
    with Manager() as manager:
        L = manager.list()
        jobs = []
        for i in range(5):
            p = Process(target=worker, args=(L,i,keyword,))
            p.start ()
            jobs.append(p)
        for p in jobs:
            p.join()
        data = [d['data'] for d in L]

        flat_list = [item for sublist in data for item in sublist]
        flat_list = [(l.get('created_time'),l.get('data')) for l in flat_list]
        res = defaultdict(list)
        for k, v in flat_list: res[k].append(v)
        res = [{'created_time': parse(k), "data": parsedata(v)} for k, v in res.items()]
        return {"keyword": keyword, "data": res}

if __name__ == '__main__':
    print getdata('narendramodi')