
from datetime import date, timedelta,datetime
from countryinfo import countries
from pytz import timezone
from django.core.cache import cache
from dateutil.parser import parse



def getdaterange(from_date,to_date):

    """
    This will return the from date and to date for getting records from database
    :param from_date: String
    :param to_date: String
    :return: dictionary



            if from date is empty string we are intializing it to None
            if to date is empty string we are intializing it to None

        case 1:

            if from date is None

                then it will return fromdate as 7days before from current date and min timestamp
                and todate as yesterday with max timestamp
        case 2 :

            if from date is not None and to date is None:

                then it will return fromdate as parsed datetime from given fromdate string
                and todate as yesterday with max timestamp
        case 3:

            if fromdate is not None and todate is not None

                then it will return fromdate as parsed datetime from given fromdate string and
                todate as parsed datetime from given to_date string

        case 4 :

            if fromdate is not None and to_date is currentdate

             then it will return fromdate as parsed datetime from given fromdate string and
             todate as parsed datetime from given to_date string m
    """
    if from_date == '':
        from_date = None
    if to_date == '':
        to_date = None

    today_date_min = datetime.combine(date.today(), datetime.min.time())
    today_date_max = datetime.combine(date.today(), datetime.max.time())

    if from_date is None:
        from_date = datetime.combine(date.today() - timedelta(7), datetime.min.time())
        to_date   = datetime.combine(date.today() , datetime.max.time())
        return {"from_date":from_date,"to_date":to_date}

    if from_date is not None and to_date is None:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.combine(date.today(), datetime.max.time())
        return {"from_date": from_date, "to_date": to_date}
    if from_date is not None and from_date == date.today().__str__():
        from_date = today_date_min
        to_date   = today_date_max
        return {"from_date": from_date, "to_date": to_date}
    if from_date is not None and to_date is not None:
        from_date = datetime.strptime(from_date, '%Y-%m-%d') # datetime(2017,07,17)
        to_date   = datetime.combine(datetime.strptime(to_date, '%Y-%m-%d').date() , datetime.max.time())
        return {"from_date": from_date, "to_date": to_date}

def getpipeline(source,key,from_date,to_date,limit=None):

    """

    This will return the pipeline for Mongodb for getting records matched with searchkey,
    and source and given date range

    :param source: String : it can be facebook, news, youtube, twitter
    :param key: String : actual search key for getting the matched data
    :param from_date: String : date as SQL format (yyyy-mm-dd)
    :param to_date: String : date as SQL format (yyyy-mm-dd)
    :param limit: Int : Number Records to fetch from database
    :return: List : pipeline
    """
    daterange = getdaterange(from_date=from_date,to_date=to_date)

    if limit:

        if source == "facebook":
            pipeline = [
                {"$match": {'created_time': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key,
                            'message': {'$ne':'null'},
                            }},
                {'$sort': {'created_time': -1}},
                {'$limit': limit},
                {'$project':{'_id':'$postid','postid':1,'type':1,'message':1,'message_parsed':1,'created_time':1,'place':1,
                             'permalink_url':1,'link':1,'picture':1,'shares':1,'comment_count':1,
                             'likes_count':1,'wows_count':1,'hahas_coun':1,'angrys_count':1,
                             'sads_count':1,'loves_count':1,'updated_time':1,'likes':1,'wows':1,
                             'loves':1,'hahas':1,'angrys':1,'comments':1,'pageinfo':1,'polarity':1,
                             'searchKey':1,'sourceType':1,'lang':1,'sads':1}},
                #{'allowDiskUse': 'true'}
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline
        if source == 'youtube':
            pipeline = [
                {"$match": {'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key
                            }},
                {'$sort': {'snippet.publishedAt': -1}},
                {'$limit': limit},
                {'$project':{'_id':'$videoId','videoId':1,'title':1,'snippet':1,'contentDetails':1,
                             'status':1,'statistics':1,'topicDetails':1
                            ,'liveStreamingDetails':1,'polarity':1,'channel':1,'comments':1,'sourceType':1,'searchKey':1}}
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline
        if source == 'twitter':
            pipeline = [
                {"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key,
                            #'lang':{'$ne':'en'},
                            }},
                {'$sort': {'created_at': -1}},
                {'$limit': limit},
                {'$project': {'_id': '$tweetid',
                              'contributors': 1, 'truncated': 1, 'text': 1,'text_parsed':1 ,'is_quote_status': 1,
                              'tweetid': 1, 'id_str': 1, 'favorite_count': 1, 'retweeted': 1,
                              'coordinates': 1, 'source': 1, 'retweet_count': 1, 'retweeted_status': 1,
                              'favorited': 1, 'lang': 1, 'created_at': 1, 'place': 1, 'entities': 1, 'user': 1, 'metadata': 1,
                              'polarity': 1, 'searchKey': 1}},
                #{'allowDiskUse': True},

                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline

        if source == 'news':
            pipeline = [
                {"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key
                            }},
                {'$sort': {'created_at': -1}},
                {'$limit': limit},
                {'$project':{'_id':'$newsid','newsid':1,'created_at':1,'link':1,'description':1,'description_parsed':1,'image':1,
                             'title':1,'source':1,'polarity':1,'searchKey':1,'sourceType':1,'lang':1}}
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline
    else :
        if source == "facebook":
            pipeline = [
                {"$match": {'created_time': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key,
                            'message': {'$ne': 'null'},
                            }},
                {'$sort': {'created_time': -1}},
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline
        if source == 'youtube':
            pipeline = [
                {"$match": {
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                    'searchKey': key
                    }},
                {'$sort': {'snippet.publishedAt': -1}},
                {'$project': {'_id': '$videoId', 'videoId': 1, 'title': 1, 'snippet': 1, 'contentDetails': 1,
                              'status': 1, 'statistics': 1, 'topicDetails': 1
                    , 'liveStreamingDetails': 1, 'polarity': 1, 'channel': 1, 'comments': 1, 'sourceType': 1,
                              'searchKey': 1}}
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
            ]
            return pipeline
        if source == 'twitter':
            pipeline = [
                {"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key
                            }},
                {'$sort': {'created_at': -1}},
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline

        if source == 'news':
            pipeline = [
                {"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': key
                            }},
                {'$sort': {'created_at': -1}},
                # {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                ]
            return pipeline

def getpipelinewithaggregation(source,key,from_date,to_date):
    """

        This will return the pipeline for Aggregation liek frequency for each day matched with searchkey,
        and source and given date range

        :param source: String : it can be facebook, news, youtube, twitter
        :param key: String : actual search key for getting the matched data
        :param from_date: String : date as SQL format (yyyy-mm-dd)
        :param to_date: String : date as SQL format (yyyy-mm-dd)
        :param limit: Int : Number Records to fetch from database
        :return: List : pipeline
        """

    daterange = getdaterange(from_date=from_date, to_date=to_date)

    if source == "facebook":
        pipeline = [{"$match": {'created_time': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                                'searchKey': key
                                }},
                    {
                        '$project': {
                            'created_time': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$created_time"}},

                        }
                    },
                     {"$group": {"_id": "$created_time", "count": {'$sum': 1}}},

                    ]
        return pipeline
    if source == 'youtube':
        pipeline = [{"$match": {'publishedat': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                                'searchKey': key
                                }},
                    {
                        '$project': {
                            'publishedat': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$publishedat"}},

                        }
                    },
                     {"$group": {"_id": "$publishedat", "count": {'$sum': 1}}},
                    ]
        return pipeline
    if source == 'twitter':
        pipeline = [{"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                                'searchKey': key
                                }},
                    {
                        '$project': {
                            'created_at': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$created_at"}},

                        }
                    },
                    {"$group": {"_id": "$created_at", "count": {'$sum': 1}}},
                    ]
        return pipeline

    if source == 'news':
        pipeline = [{"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                                'searchKey': key
                                }},
                    {
                        '$project': {
                            'created_time': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$created_at"}},

                        }
                    },
                     {"$group": {"_id": "$created_time", "count": {'$sum': 1}}},
                    ]
        return pipeline

def parseTimewithZone(date,zone):
    """
    This will rertutn the created_date as String and created
    time as String after converting the given datetime to given time zone
    :param date: datetime
    :param zone: String
    :return: dictionary
    """
    date = parse(date)
    for i in countries:
        if zone.lower() == i['code'].lower():
            tz = timezone(i['timezones'][0])
            addtime = tz.utcoffset(date.replace(tzinfo=None))
            date = date + timedelta(0,addtime.total_seconds())
            return {"created_date":date.date().__str__(),"created_time":date.time().__str__()}

def gettwittergisfields(key,tweets,zone='in'):
    """
    Return the Tweets with Required fields
    :param key: searchKey
    :param tweets: List of tweets
    :param zone: time Zone
    :return: dictionary
    """
    temptweets = []

    for tweet in tweets:
        temptweet = {}

        created = parseTimewithZone(tweet.get("created_at", ''),zone)

        temptweet["user_id"]            = tweet.get("user").get("id")
        temptweet["user_name"]          = tweet.get("user").get("name")
        temptweet["user_screenname"]    = tweet.get("user").get("screen_name",None)
        temptweet["created_date"]       = created.get("created_date")
        temptweet["created_time"]       = created.get("created_time")
        temptweet["tweet_id"]           = tweet.get("tweetid", None)
        temptweet['text']               = tweet.get('text', None)
        temptweet["longitude"]           = float(tweet.get("place", {}).get("coordinates", [])[0][0][0]) if len(
            tweet.get("place", {}).get("coordinates", [])) > 0 else 0
        temptweet["latitude"] = float(tweet.get("place", {}).get("coordinates", [])[0][0][1]) if len(
            tweet.get("place", {}).get("coordinates", [])) > 0 else 0

        temptweet['user_following']     = tweet.get('user',{}).get('friends_count')
        temptweet['user_followers']     = tweet.get('user', {}).get('followers_count')
        temptweet['total_tweets']       = tweet.get('user',{}).get('statuses_count')
        temptweet['tweet_location']     = tweet.get('place',{}).get('full_name',None)
        temptweet['tweet_location_type']= tweet.get('place',{}).get('place_type',None)
        temptweet['tweet_country']      = tweet.get('place',{}).get('country',None)
        temptweet['profile_location']   = tweet.get('user',{}).get("location",None)
        temptweet['profile_image_url']  = tweet.get('user',{}).get('profile_image_url',None)
        temptweet['profile_url']        = 'https://twitter.com/'+tweet.get('user',{}).get('screen_name')
        temptweets.append(temptweet)

    cache.set(key+'_gis',temptweets)

    return temptweets

def getDatewiseData(source,id):
    """
    It will return tghe pipeline to get the actual object
    :param source: String : f -> facebook, y -> youtube, t -> twitter, n -> news
    :param id: object id
    :return: pipeline
    """
    if source == "f":
        pipeline = [ { "$match": { 'postid': id}}, ]
        return pipeline
    if source == 'y':
        pipeline = [{"$match": {'videoid': id}},]
        return pipeline
    if source == 't':
        pipeline = [{"$match": {'tweetid': int(id)}},]
        return pipeline

    if source  == 'n':
        pipeline = [{"$match": {'newsid': id}}]
        return pipeline

def aggregatepolarity(fb, tw, yu, nw):
    """
    Retunr the cumulative polarity for the 4 objects.
    :param fb: facebook object
    :param tw: twitter object
    :param yu: Youtube object
    :param nw: News Object
    :return: dictionary
    """

    lst = [fb, tw, yu, nw]
    #count = (sum(x is not None for x in lst))

    positive = 0
    negative = 0
    neutral  = 0

    if fb is not None and fb.get('polarity').get('key') == 'positive':
        positive = positive + 1
    elif fb is not None and fb.get('polarity').get('key') == 'negative':
        negative = negative + 1
    elif fb is not None:
        neutral = neutral + 1

    if tw is not None and tw.get('polarity').get('key') == 'positive':
        positive = positive + 1
    elif tw is not None and tw.get('polarity').get('key') == 'negative':
        negative = negative + 1
    elif tw is not None:
        neutral = neutral + 1

    if yu is not None and yu.get('polarity').get('key') == 'positive':
        positive = positive + 1
    elif yu is not None and yu.get('polarity').get('key') == 'negative':
        negative = negative + 1
    elif yu is not None:
        neutral = neutral + 1

    if nw is not None and nw.get('polarity').get('key') == 'positive':
        positive = positive + 1
    elif nw is not None and nw.get('polarity').get('key') == 'negative':
        negative = negative + 1
    elif nw is not None:
        neutral = neutral + 1

    #if count == 0:
    return {"positive": positive, "negative": negative, "neutral": neutral}
    #else:
    #    return {"positive": positive / count, "negative": negative / count, "neutral": neutral / count}

def sentimentPipeline(searchKey, from_date=None, to_date=None):

    daterange = getdaterange(from_date=from_date, to_date=to_date)
    pipeline = [{"$match": {'created_at': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                            'searchKey': searchKey
                            }},
                {'$project': {'key': '$polarity.key'}},
                {'$group': {"_id": "$key", "count": {'$sum': 1}}},
                {'$project': {'key': '$_id', 'count': '$count'}}]

    return pipeline

def safe_list_get( l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default

def filterwithsubkey(data,source,subkey=None,**kwargs):

    def safesubstring(text_original, substring):

        if text_original is None:
            return -1

        try:

            return text_original.index(substring)
        except ValueError:
            return -1

    def _filterFacebookData(posts, subkey=None,**kwargs):

        daterange = getdaterange(from_date=kwargs['from_date'], to_date=kwargs['to_date'])

        if subkey:
            tempdata = []
            for post in posts:
                tweettime = int(post.get('created_time').date().strftime('%s'))
                message = post.get('message_parsed')
                if safesubstring(message, subkey) != -1 and (
                                tweettime >= int(daterange.get("from_date").date().strftime('%s'))
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s'))):
                    tempdata.append(post)
            return tempdata
        else:
            tempdata = []
            for post in posts:
                tweettime = int(post.get('created_time').date().strftime('%s'))
                if tweettime >= int(daterange.get("from_date").date().strftime('%s')) \
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s')):
                    tempdata.append(post)
            return tempdata

    def _filterTwitterData(tweets, subkey=None,**kwargs):

        daterange = getdaterange(from_date=kwargs['from_date'],to_date=kwargs['to_date'])

        if subkey:
            tempdata = []
            for tweet in tweets:
                tweettime = int(parse(tweet.get('created_at')).date().strftime('%s'))
                message = tweet.get('text_parsed')
                if safesubstring(message,subkey) != -1 and (
                                tweettime >= int(daterange.get("from_date").date().strftime('%s')) \
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s'))):

                    tempdata.append(tweet)
            return tempdata
        else:
            tempdata = []
            for tweet in tweets:
                tweettime = int(parse(tweet.get('created_at')).date().strftime('%s'))
                if tweettime >= int(daterange.get("from_date").date().strftime('%s')) \
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s')):
                    tempdata.append(tweet)
            return tempdata

    def _filterYoutubeData(videos, subkey=None,**kwargs):

        daterange = getdaterange(from_date=kwargs['from_date'], to_date=kwargs['to_date'])
        
        if subkey:
            tempdata = []
            for video in videos:
                tweettime = int(parse(video.get('snippet').get('publishedAt')).date().strftime('%S'))
                message = video.get('snippet').get('descriptionParsed')
                if safesubstring(message, subkey) != -1 and (
                                tweettime >= int(daterange.get("from_date").date().strftime('%S'))
                        and tweettime <= int(daterange.get("to_date").date().strftime('%S'))):
                    tempdata.append(video)
            return tempdata
        else:
            tempdata = []
            for video in videos:
                tweettime = int(parse(video.get('snippet').get('publishedAt')).date().strftime('%S'))
                if tweettime >= int(daterange.get("from_date").date().strftime('%S')) \
                        and tweettime <= int(daterange.get("to_date").date().strftime('%S')):
                    tempdata.append(video)
            return tempdata

    def _filterNewsData(news, subkey=None,**kwargs):
        daterange = getdaterange(from_date=kwargs['from_date'], to_date=kwargs['to_date'])

        if subkey:
            tempdata = []
            for article in news:
                tweettime = int(article.get('created_at').date().strftime('%s'))
                message = article.get('description_parsed')
                if safesubstring(message, subkey) != -1 and (
                                tweettime >= int(daterange.get("from_date").date().strftime('%s'))
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s'))):
                    tempdata.append(article)
            return tempdata
        else:
            tempdata = []
            for article in news:
                tweettime = int(article.get('created_at').date().strftime('%s'))
                if tweettime >= int(daterange.get("from_date").date().strftime('%s')) \
                        and tweettime <= int(daterange.get("to_date").date().strftime('%s')):
                    tempdata.append(article)
            return tempdata

    if source == 'twitter':
        return _filterTwitterData(data, subkey=subkey,**kwargs)
    if source == 'facebook':
        return _filterFacebookData(data, subkey=subkey,**kwargs)
    if source == 'youtube':
        return _filterYoutubeData(data, subkey=subkey,**kwargs)
    if source == 'news':
        return _filterNewsData(data, subkey=subkey,**kwargs)


def getYoutubePiplines(searchKey,from_date,to_date,subkey=None):
    daterange = getdaterange(from_date=from_date, to_date=to_date)

    if subkey:
        return  {'statisitcs': [
                            {'$match':{
                                'searchKey': searchKey,
                                'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                                'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
                            }},
                            {'$project':{'id': '$searchKey','statistics': '$statistics','contentDetails': '$contentDetails',
                            'live': {'$cond': { 'if': { '$gt': ['$liveStreamingDetails', {}]}, 'then': 1, 'else': 0}}
                            }},
                    {'$group':{'_id': '$id', 'viewCount': {'$sum':'$statistics.viewCount'},
                    'likeCount':{'$sum':'$statistics.likeCount'},
                    'dislikeCount':{'$sum':'$statistics.dislikeCount'},
                    'commentCount':{'$sum':'$statistics.commentCount'},
                    'totalDuration':{'$sum':'$contentDetails.duration'},
                    'liveVideos': {'$sum':'$live'}
                    }}
        ],
        'categorywise':[
            {'$match': {
                'searchKey': searchKey,
                'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
            }},
                        {'$group':{'_id':'$snippet.categoryId','count':{'$sum':1}}},
        ],
        'channelwise':[
            {'$match': {
                'searchKey': searchKey,
                'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
            }},
            {'$group':{'_id': {'channelId': '$channel.channelId', 'title': '$channel.snippet.title'}, 'count': {'$sum':1}}}
        ],
        'commentSentiment':[
            {'$match': {
                'searchKey': searchKey,
                'comments.0': {'$exists': True},
                'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
            }},
                        {"$project": {'searchKey':'$searchKey','comment':'$comments' }},
                        {"$unwind": "$comment" },
                        {'$group':{'_id':'$comment.polarity.key','count':{'$sum':1}}}
        ],
        'videosSentiment':[
            {'$match': {
                'searchKey': searchKey,
                'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
            }},
            {'$group': {'_id': '$polarity.key', 'count': {'$sum':1}}}
        ],
            'counts': [
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                    'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
                }},
                {'$group': {'_id': '$searchKey', 'count': {'$sum': 1}}}
            ],

            'videoScores':[
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                    'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
                }},
                {'$project': {
                    'searchKey': '$searchKey',
                    'fair': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0]}, {'$lt': ["$polarity.value", 0.25]}]}, 1,
                                  0]},
                    'good': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0.25]}, {'$lt': ["$polarity.value", 0.5]}]}, 1,
                                  0]},
                    'excellent': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0.5]}, {'$lt': ["$polarity.value", 1]}]}, 1,
                                  0]},
                    'bad': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", -0.5]}, {'$lt': ["$polarity.value", 0]}]}, 1,
                                  0]},
                    'verybad': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", -1]}, {'$lt': ["$polarity.value", -0.5]}]}, 1,
                                  0]},
                    'other': {'$cond': [{'$eq': ["$polarity.value", 0]}, 1, 0]},
                }},
                {'$group': {
                    '_id': '$searchKey',
                    'faircount': {'$sum': '$fair'},
                    'goodcount': {'$sum': '$good'},
                    'excellentcount': {'$sum': '$excellent'},
                    'badcount': {'$sum': '$bad'},
                    'verybadcount': {'$sum': '$verybad'},
                    'othercount': {'$sum': '$other'}}}
            ],
            'description': [
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                    'snippet.descriptionParsed': {'$regex': r'\b{}\b'.format(subkey), '$options': 'i'}
                }},
                {
                    '$group':
                        {
                            '_id': '$searchKey', 'description': {'$push': '$snippet.descriptionParsed'}
                        }
                }
            ]


        }
    else:
        return {'statisitcs': [
            {'$match': {'searchKey': searchKey,
                        'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")}}},
            {'$project': {'id': '$searchKey', 'statistics': '$statistics', 'contentDetails': '$contentDetails',
                          'live': {'$cond': {'if': {'$gt': ['$liveStreamingDetails', {}]}, 'then': 1, 'else': 0}}
                          }},
            {'$group': {'_id': '$id', 'viewCount': {'$sum': '$statistics.viewCount'},
                        'likeCount': {'$sum': '$statistics.likeCount'},
                        'dislikeCount': {'$sum': '$statistics.dislikeCount'},
                        'commentCount': {'$sum': '$statistics.commentCount'},
                        'totalDuration': {'$sum': '$contentDetails.duration'},
                        'liveVideos': {'$sum': '$live'}
                        }}
        ],
            'categorywise': [
                {'$match': {'searchKey': searchKey, 'snippet.publishedAt': {"$lte": daterange.get("to_date"),
                                                                            "$gte": daterange.get("from_date")}}},
                {'$group': {'_id': '$snippet.categoryId', 'count': {'$sum': 1}}},
            ],
            'channelwise': [
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"),"$gte": daterange.get("from_date")}}},
                {'$group': {'_id': {'channelId': '$channel.channelId', 'title': '$channel.snippet.title'},
                            'count': {'$sum': 1}}},
            ],
            'commentSentiment': [
                {"$match": {'searchKey': searchKey, 'comments.0': {'$exists': True},
                            'snippet.publishedAt': {"$lte": daterange.get("to_date"),
                                                    "$gte": daterange.get("from_date")}}},
                {"$project": {'searchKey': '$searchKey', 'comment': '$comments'}},
                {"$unwind": "$comment"},
                {'$group': {'_id': '$comment.polarity.key', 'count': {'$sum': 1}}}
            ],
            'videosSentiment': [
                {'$match': {'searchKey': searchKey,
                            'snippet.publishedAt': {"$lte": daterange.get("to_date"),
                                                    "$gte": daterange.get("from_date")}}},
                {'$group': {'_id': '$polarity.key', 'count': {'$sum': 1}}}
            ],
            'counts': [
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                }},
                {'$group': {'_id': '$searchKey', 'count': {'$sum': 1}}}
            ],
            'videoScores': [
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                }},
                {'$project': {
                    'searchKey': '$searchKey',
                    'fair': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0]}, {'$lt': ["$polarity.value", 0.25]}]}, 1,
                                  0]},
                    'good': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0.25]}, {'$lt': ["$polarity.value", 0.5]}]}, 1,
                                  0]},
                    'excellent': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", 0.5]}, {'$lt': ["$polarity.value", 1]}]}, 1,
                                  0]},
                    'bad': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", -0.5]}, {'$lt': ["$polarity.value", 0]}]}, 1,
                                  0]},
                    'verybad': {
                        '$cond': [{'$and': [{'$gt': ["$polarity.value", -1]}, {'$lt': ["$polarity.value", -0.5]}]}, 1,
                                  0]},
                    'other': {'$cond': [{'$eq': ["$polarity.value", 0]}, 1, 0]},
                }},
                {'$group': {
                    '_id': '$searchKey',
                    'faircount': {'$sum': '$fair'},
                    'goodcount': {'$sum': '$good'},
                    'excellentcount': {'$sum': '$excellent'},
                    'badcount': {'$sum': '$bad'},
                    'verybadcount': {'$sum': '$verybad'},
                    'othercount': {'$sum': '$other'}}}
            ],

            'description':[
                {'$match': {
                    'searchKey': searchKey,
                    'snippet.publishedAt': {"$lte": daterange.get("to_date"), "$gte": daterange.get("from_date")},
                }},
                {
                    '$group':
                        {
                            '_id': '$searchKey', 'description': {'$push': '$snippet.descriptionParsed'}
                        }
                }
            ]
        }

def getTwitterPipelines(searchKey,from_date,to_date,subkey=None):
    daterange = getdaterange(from_date,to_date)

    return {

        "statistics":[
                    {
                    '$match':{
                        'searchKey': searchKey,
                        'created_at': {'$lte': daterange.get('from_date'), '$gte': daterange.get('to_date')}
                        }
                    },
                    # {
                    #   '$group': {
                    #     '_id': 'tweets',
                    #     'tweetCount'   : {'$sum': {'$cond': [{'$eq': ["$retweet_count", 0]}, 1, 0]}},
                    #     "retweetCount" : {'$sum': {'$cond': [{'$ne': ["$retweet_count", 0]}, 1, 0]}},
                    #     "mentionsCount": {'$sum': {'$cond': [{'$ne': [{'$size': '$entities.user_mentions'}, 0]}, 1, 0]}},
                    #     'hashTagsCount': {'$sum': {'$cond': [{'$ne': [{'$size': '$entities.hashtags'}, 0]}, 1, 0]}},
                    #     'users'        : {'$addToSet': '$user.screen_name'},
                    #     }
                    # },
                    # {
                    #     '$project': {
                    #     'tweets'  : '$tweetCount',
                    #     'retweets': '$retweetCount',
                    #     'mentions': '$mentionsCount',
                    #     'hashTags': '$hashTagsCount',
                    #     'authors' : {'$size': '$users'}
                    # }}
        ]

    }
