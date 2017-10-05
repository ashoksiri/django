
from TwitterAPI import TwitterAPI
import json,time,itertools,operator
from sentimentUtils import SentimentUtils
from bson import json_util
from dateutil.parser import *
from datetime import datetime
from collections import defaultdict

#CONSUMER_KEY = '8oreMpLNqYf7NessspKe81esH'
#CONSUMER_SECRET = 'oxyRKpaLYGRLICSmHlwMuBWgaAK9Q12UmYlT1roxLRyXUJuziW'
#ACCESS_TOKEN_KEY = '838690575146692608-WlA6eR0ELIDITHWtIQLJKSuOroKpK4k'
#ACCESS_TOKEN_SECRET = 'Jl3xHAK8ZVDlupWR3dxY6N6LidINC9dEgWmdNRqK8oCHN'

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

    def parseMentions(self,mentions):
        tempmentions = []
        for mention in mentions:
            tempmentions.append({
                "screen_name" : mention.get("screen_name",None),
                "id"          : mention.get("id_str",None),
                "name"        : mention.get("name",None)
            })

        return tempmentions

    def parsePlace(self,place):
        if place is not None:
            return {
                "id"            : place.get("id",None),
                "country_code"  : place.get("country_code",None),
                "country"       : place.get("country",None),
                "place_type"    : place.get("place_type",None),
                "coordinates"   : place.get("bounding_box",{}).get("coordinates",[]),
                "full_name"     : place.get("full_name",None),
                "name"          : place.get("name",None)
                }
        else:
            return {}

    def parseUser(self,user):

        if user is not None:
            return {

                "id"                      :user.get("id_str"),
                "time_zone"               : user.get("time_zone",None),
                "profile_image_url_https" : user.get("profile_image_url_https",None),
                "geo_enabled"             : user.get("geo_enabled",False),
                "followers_count"         : user.get("followers_count",0),
                "listed_count"            : user.get("listed_count",0),
                "lang"                    : user.get("lang",None),
                "statuses_count" : user.get("statuses_count",0),
                "friends_count" : user.get("friends_count",0),
                "profile_image_url" : user.get("profile_image_url",None),
                "profile_banner_url" : user.get("profile_banner_url",None),
                "name"               : user.get("name",None),
                "screen_name"        : user.get("screen_name",None),
                "url"                : user.get("url",None),
                "created_at"         : parse(user.get("created_at",None)) if user.get("created_at",None) != None else datetime.min,
                "location"           : user.get("location",None),



            }
        else:
            return {}


    def parseTweet(self,tweets):
        tempTweets = []

        for tweet in tweets:
            tempTweets.append({

                "tweetid"        : tweet.get("id"),
                "text"           : tweet.get("text",None),
                "lang"           : tweet.get("lang",None),
                "geo"            : tweet.get("geo",{}),
                "created_at"     : parse(tweet.get("created_at",None)) if tweet.get("created_at",None) != None else datetime.min,
                "user"           : self.parseUser(tweet.get("user",{})),
                "place"          : self.parsePlace(tweet.get("place",{})),
                "retweet_count"  : tweet.get("retweet_count",0),
                "favorite_count" : tweet.get("favorite_count",0),
                "user_menstions" : self.parseMentions(tweet.get("entities",{}).get("user_mentions",[])),
                "tags"           : tweet.get("entities",{}).get("hashTags",[]),
                "polarity"       : sutils.get_sentiment(tweet.get("text",None)),

            })

        tempTweets = [(tweet.get('created_at').date().__str__(),tweet) for tweet in tempTweets]

        res = defaultdict(list)
        for k, v in tempTweets: res[k].append(v)
        res = [{'created_time': k, "data":{"twitter":{"tweets":v}}} for k, v in res.items()]
        return res

    def getTweets(self,searchKey,lang=''):

        tweets =  api.request('search/tweets', {'q': searchKey,'count':20,'lang':lang})

        return {"keyword":searchKey,"data":self.parseTweet(tweets)}




if __name__ == "__main__":
    utils = TwitterUtils()
    print json.dumps(utils.getTweets(searchKey="@rahul_msritgis"),default=json_util.default)
