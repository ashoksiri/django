from apiclient.http import BatchHttpRequest
from apiclient.discovery import build
import json
from sentimentUtils import SentimentUtils
from dateutil.parser import *
import datetime
from bson import json_util
from collections import defaultdict


DEVELOPER_KEY="AIzaSyBpWXegO6Vp9-73v8ifTA1kjwchGeXRj2E"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"



youtube =  build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
sutils = SentimentUtils()


class YoutubeUtils(object):

    videos = []

    def comments( self,request,response,exception):
        if response is not None:
            for video in self.videos:
                if len(response['items']) > 0:
                    if video['videoid'] == response['items'][0].get('snippet',{}).get('videoId','NA'):
                        #print json.dumps(response,indent=2)
                        video['comments'] = []
                        for item in response['items']:
                            published = item['snippet']['topLevelComment']['snippet'].get('publishedAt', 'NA')
                            video['comments'].append(
                            {"commentid":item['snippet']['topLevelComment'].get('id','NA'),
                             "userid":item['snippet']['topLevelComment']['snippet']['authorChannelId'].get('value','NA'),
                             "username" : item['snippet']['topLevelComment']['snippet'].get('authorDisplayName','NA'),
                             "publishedat": parse(published) if published != 'NA' else datetime.min,
                             "text": item['snippet']['topLevelComment']['snippet'].get('textOriginal', 'NA'),
                             "videoid":item['snippet'].get('videoId')})

                            #print item['snippet']['topLevelComment']['snippet']['authorChannelId'].get('value','NA')




    def videoStats(self,request, response,exception):
        if response is not None:
            for video in self.videos:
                if len(response.get('items',None)) > 0 and video['videoid'] == response['items'][0]['id']:
                    items = response['items'][0]
                    video['commentcount'] = items['statistics'].get('commentCount','0')
                    video['viewscount'] = items['statistics'].get('viewCount','0')
                    video['favoritecount'] = items['statistics'].get('favoriteCount','0')
                    video['dislikescount']= items['statistics'].get('dislikeCount','0')
                    video['likescount'] = items['statistics'].get('likeCount','0')



    def channelInfo(self,request,response,exception):

        #print request

        if response is not None:
            for video in self.videos:
                if video['channelid'] == response['items'][0]['id']:
                    items = response['items'][0]
                    video['chennelinfo'] = {"videoid" : video['videoid'],
                           "channelid":items['id'],
                           "channeltitle" : items['snippet']['title'],
                           "channelurl" : "https://www.youtube.com/"+items['snippet'].get('customUrl') if items['snippet'].get('customUrl','NA') is not 'NA' else 'NA',
                           "createdat" : parse(items['snippet']['publishedAt']),
                           "channeldescription" : items['snippet']['description'] if items['snippet'].get('description','NA') is not 'NA' else 'NA',
                           "commentcount" : items['statistics']['commentCount'],
                           "viewcount": items['statistics']['viewCount'],
                           "videocount": items['statistics']['videoCount'],
                           "subscriberCount": items['statistics']['subscriberCount'],
                           }
                    #print items['snippet']['description']

    def sortvideosbychannel(self,videos):
        videos = [(video.get('channelid'),video) for video in videos]
        res = defaultdict(list)
        for k, v in videos: res[k].append(v)
        res = [{'channel': k, "videos": v} for k, v in res.items()]
        return res

    def getvideos(self,q,n=5):

        search_response = youtube.search().list(q=q,part="id,snippet",maxResults=n,order='viewCount',type='video').execute()
        batch = youtube.new_batch_http_request()

        for search_result in search_response:

            if 'items' in search_result :
                for item in search_response[search_result]:

                    video_polarity = sutils.get_sentiment(item['snippet'].get('description','NA'))

                    self.videos.append({"videoid"   :item['id']['videoId'],
                                        "title"     :item['snippet']['title'],
                                        "videodiscription": item['snippet']['description'],
                                        "videourl"  : "https://www.youtube.com/watch?v="+item['id']['videoId'],
                                        "publishedat":parse(item['snippet']['publishedAt']),
                                        "polarity"  : video_polarity,
                                        "lanng"     : sutils.detect_language(item['snippet'].get('description','NA')),
                                        "channelid" : item['snippet']['channelId'],
                                        "image"     : item['snippet']['thumbnails']['default']['url']
                                        })

                    batch.add(youtube.commentThreads().list(part="id,snippet",videoId=item['id']['videoId'],maxResults=50,textFormat='plainText'),callback=self.comments)
                    batch.add(youtube.videos().list(part="statistics,status,recordingDetails",id=item['id']['videoId'],maxResults=50),callback=self.videoStats)
                    batch.add(youtube.channels().list(part="snippet,contentDetails,statistics,topicDetails,brandingSettings,status", id=item['snippet']['channelId'], maxResults=50),callback=self.channelInfo)

        batch.execute()
        videos = self.videos
        videos = [(video.get('publishedat').date().__str__(),video ) for video in videos]
        res = defaultdict(list)
        for k, v in videos: res[k].append(v)
        res = [{'created_time': k, "data":{"youtube":{"channel":self.sortvideosbychannel(v)}}} for k, v in res.items()]
        return {"keyword":q,"data":res}

if __name__ == "__main__":
    yutils = YoutubeUtils()
    print json.dumps(yutils.getvideos(q='GST'),indent=2,default=json_util.default)

