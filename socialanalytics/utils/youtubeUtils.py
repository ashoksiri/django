
import apiclient

from apiclient.http import BatchHttpRequest
from apiclient.discovery import build
import json
from dateutil.parser import *
import datetime
from bson import json_util
from collections import defaultdict
from httplib2 import Http
from socialanalytics.utils.sentimentUtils import SentimentUtils
from isodate import parse_duration
DEVELOPER_KEY="AIzaSyBpWXegO6Vp9-73v8ifTA1kjwchGeXRj2E"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"
sutils = SentimentUtils()

youtube =  build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

channelSnippet = "brandingSettings,contentDetails,contentOwnerDetails,id,invideoPromotion,localizations,snippet,statistics,status,topicDetails"
videoSnippet = "contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails"
commentSnippet = "id,snippet"

def getvideos(q, n=10):
    videos = []
    def comments(request, response, exception):
        if response is not None:
            commentsList = []
            for video in videos:
                if len(response['items']) > 0:
                    if video['videoId'] == response['items'][0].get('snippet', {}).get('videoId', None):
                        for item in response['items']:
                            snippet = item['snippet']
                            snippet.__setitem__('channelId', video['channelId'])
                            commentSnippet = snippet['topLevelComment']['snippet']
                            commentText = commentSnippet['textOriginal']
                            commentTextParsed = sutils.get_sentiment(commentText)
                            commentSnippet['textOriginalParsed'] = commentTextParsed['text']
                            snippet['topLevelComment']['snippet'] = commentSnippet
                            snippet['topLevelComment']['snippet']['channelId'] = video['channelId']

                            commentsList.append({'commentId': item['id'],
                                                 'snippet': snippet,
                                                 'polarity': commentTextParsed['polarity']})
                        video['comments'] = commentsList

    def videoStats(request, response, exception):
        if response is not None:
            for video in videos:
                if len(response.get('items', None)) > 0 and video['videoId'] == response['items'][0]['id']:
                    item = response['items'][0]
                    videoSnippet = item['snippet']
                    videoPolarity = sutils.get_sentiment(videoSnippet.get('description', None))
                    videoSnippet['descriptionParsed'] = videoPolarity.get('text')
                    video['snippet'] = videoSnippet
                    video['contentDetails'] = item.get('contentDetails', None)
                    video['contentDetails']['duration'] = int(
                        parse_duration(item.get('contentDetails').get('duration')).total_seconds())
                    video['status'] = item.get('status', {})
                    video['statistics'] = item.get('statistics', {})
                    video['topicDetails'] = item.get('topicDetails', {})
                    video['liveStreamingDetails'] = item.get('liveStreamingDetails', {})
                    video['polarity'] = videoPolarity.get('polarity')

    def channelInfo(request, response, exception):
        if response is not None:
            for video in videos:
                channelInfoDict = {}
                if len(response.get('items', None)) > 0 and video['channelId'] == response['items'][0]['id']:
                    item = response['items'][0]
                    if item['id'] in channelInfoDict.keys():
                        video['channel'] = channelInfoDict[item['id']]
                    else:
                        channel = {'channelId': item['id'], 'snippet': item['snippet'],
                                   'contentDetails': item.get('contentDetails', {}),
                                   'statistics': item.get('statistics', {}),
                                   'topicDetails': item.get('topicDetails', {}),
                                   'status': item.get('status', {}),
                                   'brandingSettings': item.get('brandingSettings', {}),
                                   'contentOwnerDetails': item.get('contentOwnerDetails', {})}
                        channelInfoDict[item['id']] = channel
                        video['channel'] = channel

        if exception is not None:
            print exception

    search_response = youtube.search().list(q=q, part="id,snippet", maxResults=n, order='date',type='video',regionCode='IN').execute()
    top_videos = youtube.search().list(q=q, part="id,snippet", maxResults=n, order='viewCount', type='video',
                                            regionCode='IN').execute()
    batch = youtube.new_batch_http_request()

    for search_result in search_response:

        if 'items' in search_result:
            for item in search_response[search_result]:
                videos.append({"videoId": item['id']['videoId'],
                               "title": item['snippet']['title'],
                               "channelId": item['snippet']['channelId'],
                               })
                batch.add(youtube.commentThreads().list(part=commentSnippet, videoId=item['id']['videoId'], maxResults=50, textFormat='plainText'), callback=comments)
                batch.add(youtube.videos().list(part=videoSnippet, id=item['id']['videoId'],maxResults=30), callback=videoStats)
                batch.add(youtube.channels().list(part=channelSnippet,id=item['snippet']['channelId'], maxResults=30), callback=channelInfo)

    for search_result in top_videos:

        if 'items' in search_result:
            for item in top_videos[search_result]:
                videos.append({"videoId": item['id']['videoId'],
                               "title": item['snippet']['title'],
                               "channelId": item['snippet']['channelId'],
                               })
                batch.add(youtube.commentThreads().list(part=commentSnippet, videoId=item['id']['videoId'], maxResults=50, textFormat='plainText'), callback=comments)
                batch.add(youtube.videos().list(part=videoSnippet, id=item['id']['videoId'],maxResults=30), callback=videoStats)
                batch.add(youtube.channels().list(part=channelSnippet,id=item['snippet']['channelId'], maxResults=30), callback=channelInfo)

    batch.execute()

    return videos