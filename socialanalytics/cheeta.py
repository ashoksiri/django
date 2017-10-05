import mongoengine
from socialanalytics.models.youtubemodels import Video
from mongoengine.queryset.visitor import Q
from datetime import datetime
import isodate
from socialanalytics.utils.filtermodels import getdaterange

db = mongoengine.connect(db='db_apsma2',host='10.1.7.49')
daterange = getdaterange(from_date='2017-10-01',to_date='2017-10-13')

print daterange
pipeline = [
                {"$match": {
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                    'searchKey': 'narendramodi'
                    }},
                # {'$sort': {'snippet.publishedat': -1}},
                # {'$project': {'_id': '$videoId', 'videoId': 1, 'title': 1, 'snippet': 1, 'contentDetails': 1,
                #               'status': 1, 'statistics': 1, 'topicDetails': 1
                #     , 'liveStreamingDetails': 1, 'polarity': 1, 'channel': 1, 'comments': 1, 'sourceType': 1,
                #               'searchKey': 1}}
                # {"$group": {"_id": "$publishedat", "count": {"$sum": 1}}},
            ]

print [d for d in Video.objects.aggregate(*pipeline)]
