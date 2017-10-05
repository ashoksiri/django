
"""
    This Utils package is responsible for getting the tweets from twitter
    api matched with searchkey and convert the response as database structure

"""

from TwitterAPI import TwitterAPI
from sentimentUtils import SentimentUtils
from dateutil.parser import *
from datetime import datetime
from collections import Counter


CONSUMER_KEY = "HUdPNNybEhKOIuptZN7HHvas5"
CONSUMER_SECRET = "aj5anOLCpLuZLlBKqCB9i8GaLu3e2FsZTE1EZznqLQvk5T72TM"
ACCESS_TOKEN_KEY = "804511329302114304-h2xkzpVUlatP0aAS3eJyTHWv01ZfvPr"
ACCESS_TOKEN_SECRET = "wOf3NkiF2CtV4vpyWSSZPnyxCPaCr2zOFLUcJbn2A3pE2"

api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

sutils = SentimentUtils()

class TwitterUtils(object):


    def parsedata(self,tweet):
        contributors        = tweet.get('contributors') if tweet.get('contributors') else []
        entities            = tweet.get('entities') if tweet.get('entities') else {}
        coordinates         = tweet.get('coordinates') if tweet.get('coordinates') else {}
        retweeted_status    = self.parsedata(tweet.get('retweeted_status')) if tweet.get('retweeted_status') else {}
        user                = tweet.get('user') if tweet.get('user') else {}
        user['created_at']  = parse(user['created_at']).__str__() if user.has_key('created_at') else None
        place               = tweet.get('place') if tweet.get('place') else {}
        polarity            = sutils.get_sentiment(tweet.get('text'))

        return {'contributors'              : contributors,
                'truncated'                 : tweet.get('truncated'),
                'text'                      : tweet.get('text'),
                'text_parsed'               : polarity.get('text'),
                'is_quote_status'           : tweet.get('is_quote_status'),
                'in_reply_to_status_id'     : tweet.get('in_reply_to_status_id'),
                'tweetid'                   : tweet.get('id'),
                'favorite_count'            : tweet.get('favorite_count'),
                'entities'                  : entities,
                'coordinates'               : coordinates,
                'retweeted'                 : tweet.get('retweeted'),
                'source'                    : tweet.get('source'),
                'in_reply_to_screen_name'   : tweet.get('in_reply_to_screen_name'),
                'in_reply_to_user_id'       : tweet.get('in_reply_to_user_id'),
                'retweet_count'             : tweet.get('retweet_count'),
                'id_str'                    : tweet.get('id_str'),
                'retweeted_status'          : retweeted_status,
                'user'                      : user,
                'in_reply_to_user_id_str'   : tweet.get('in_reply_to_user_id_str'),
                'lang'                      : tweet.get('lang'),
                'created_at'                : parse(tweet.get('created_at')).__str__(),
                'in_reply_to_status_id_str' : tweet.get('in_reply_to_status_id_str'),
                'place'                     : place,
                'metadata'                  : tweet.get('metadata'),
                'polarity'                  : polarity.get('polarity')
                }

    def getTweetswithAll(self,searchKey,lang=''):
        tweets = api.request('search/tweets', {'q': searchKey, 'count': 100, 'lang': lang,'result_type':'recent'})
        temptweets = []
        for tweet in tweets:
            temptweets.append(self.parsedata(tweet))
        return temptweets

if __name__ == "__main__":
    utils = TwitterUtils()
    import json
    print json.dumps(utils.getTweetswithAll(searchKey='@ashoksiri01'))