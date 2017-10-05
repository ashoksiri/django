
"""
    This utill package is used to get the facebook data from the facebook Graph Api and parse
    the information according to the database structure.

    First we need to get the access token for facebook by creating a app at
    http://developer.facebook.com

    and get the app_id , app_secret and access_token for the app the configure the access_token in the app

"""

import time,json,urllib
from urllib2 import urlopen, Request
from sentimentUtils import SentimentUtils
from dateutil.parser import *
from datetime import datetime
from bson import json_util

sutils = SentimentUtils()

class FetchFacebookData(object):

    access_token='1257032691047126|mP2cUAf8cIH-ZA0WntiqScJT8HI'

    def request_until_succeed(self,url):
        """
        This method will call the url and get the Response as json.
        :param url: formed url for get the required fields from the facebook graph api
        :return: json response from Grapj Api
        """
        req = Request(url)
        success = False
        while success is False:
            try:
                response = urlopen(req)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                print(e)
                time.sleep(5)
                print(e.message)
                print("Retrying.")

        return response.read()

    def getpageFileds(self):
        """
        This will return some facebook page fields ',' delimitted
        :return: formed String with field params
        """

        edge = "id,about,fan_count,bio,category,company_overview,contact_address,"
        edge = edge + "current_location,description,description_html,general_info,likes,link,"
        edge = edge + "location,new_like_count,name,phone,rating_count,talking_about_count,website,"
        edge = edge + "were_here_count,"
        return edge

    def getpostFields(self,type='post'):
        """
        This will return post and comment params.
        :param type: if type is post then picture field is added
        :return: formed string with params
        """

        edge = "posts.limit(10){id,from,created_time,"
        edge = edge + "message,icon,link,permalink_url,place,type,to,updated_time,full_picture,postreactions,"
        if type == 'post' :
            edge = edge+'picture'
        edge = edge+"}"

        return edge

    def getReactionsFields(self):
        """
        This will return Reaction params , shares , comments params  for the post
        :return: formed string with field params
        """

        likes    = "reactions.type(LIKE).limit(50).summary(total_count).as(like),"
        loves    = "reactions.type(LOVE).limit(50).summary(total_count).as(love),"
        wows     = "reactions.type(WOW).limit(50).summary(total_count).as(wow),"
        hahas    = "reactions.type(HAHA).limit(50).summary(total_count).as(haha),"
        sads     = "reactions.type(SAD).limit(50).summary(total_count).as(sad),"
        angrys   = "reactions.type(ANGRY).limit(50).summary(total_count).as(angry),"
        comments = "comments.limit(50).summary(total_count),"
        shares   = "shares"

        edge = likes+loves+wows+hahas+sads+angrys+comments+shares

        return edge

    def parseLocation(self,location):
        """
        This will return dictionary of the location having below fields.
        if values presented in the given location the fields will be sent if not None values will be sent
        :param location: dictionary
        :return: dictionary
        """

        return {'city'          : location.get('city',None),
                'city_id'       : location.get('city_id',None),
                'country'       : location.get('country', None),
                'country_code'  : location.get('country_code', None),
                'latitude'      : location.get('latitude', None),
                'located_in'    : location.get('located_in', None),
                'longitude'     : location.get('longitude', None),
                'name'          : location.get('name', None),
                'region'        : location.get('region', None),
                'region_id'     : location.get('region_id', None),
                'state'         : location.get('state', None),
                'street'        : location.get('street', None),
                'zip'           : location.get('zip', None),
        }

    def parseComments(self,comments):
        """
        This will prase the comment from given comment list.
        :param comments: list of dictionary
        :return: list of dictionsry
        """
        tempcomments = []

        for comment in comments:

            polarity = sutils.get_sentiment(comment.get("message"),None)

            tempcomment =  {     "created_time"    :parse(comment.get("created_time",None)) if comment.get("created_time",None) != None else datetime.min,
                                 "message"         :comment.get("message",None),
                                 "message_parsed"  :polarity.get('text'),
                                 "polarity"        :polarity.get('polarity'),
                                 "from_user"       :comment.get("from",{}).get("name",None),
                                 "from_id"         :comment.get("from",{}).get("id",None),
                                 "commentid"       :comment.get("id",None)}
            tempcomments.append(tempcomment)
        return tempcomments

    def parseResponse(self,pages):
        """
        This will return list of posts , Facebook page information and this will embedded in the facebook post
        :param pages: List of facebok pages
        :return: list of facebook posts
        """
        tempposts = []
        for page in pages:
            temppage = {
                    "pageid"             :page['id'],
                    "about"              :page.get('about',None),
                    "fan_count"          :page.get('fan_count',None),
                    "category"           :page.get('category',None),
                    "company_overview"   :page.get('company_overview',None),
                    "contact_address"    :page.get('contact_address',None),
                    'current_location'   :page.get('current_location',None),
                    "description"        :page.get('description',None),
                    "description_html"   :page.get('description_html',None),
                    "general_info"       :page.get("general_info",None),
                    #"likes"              :page.get('likes',None),
                    "link"               :page.get("link",None),
                    "location"           :self.parseLocation(page.get('location',{})),
                    "new_like_count"     :page.get('new_like_count',None),
                    "name"               :page.get("name",None),
                    "phone"              :page.get("phone",None),
                    "rating_count"       :page.get('rating_count',None),
                    "talking_about_count":page.get('talking_about_count',None),
                    "website"            :page.get("website",None),
                    "were_here_count"    :page.get("were_here_count",None),
                    'bio'                :page.get('bio',None)
                    }

            for post in page.get('posts',{}).get('data',[]):

                message = post.get("message",None)
                polarity = sutils.get_sentiment(message)

                tempposts.append({
                    "postid"            : post.get('id',None),
                    "from_user"         : post.get('from',{}).get('name',None),
                    "from_user_id"      : post.get("from",{}).get("id",None),
                    "created_time"      : parse(post.get("created_time",None)) if post.get("created_time",None) != None else datetime.min,
                    "message"           : message,
                    "message_parsed"    : polarity.get('text'),
                    "polarity"          : polarity.get('polarity'),
                    "link"              : post.get("link",None),
                    "permalink_url"     : post.get("permalink_url",None),
                    "type"              : post.get("type",None),
                    "to_user_id"        : post.get("to",{}).get("id",None),
                    "to_user_name"      : post.get("to",{}).get("name",None),
                    "updated_time"      : parse(post.get("updated_time",None)) if post.get("updated_time",None) != None else datetime.min,
                    "full_picture"      : post.get("full_picture",None),
                    "place"             : self.parseLocation(post.get("place",{})),
                    "picture"           : post.get("picture",None),
                    "comments"          : self.parseComments(post.get("comments",{}).get("data",[])),
                    "comment_count"     : post.get("comments",{}).get("summary",{}).get("total_count",None),
                    "shares"            : post.get("shares",{}).get("count",None),
                    "likes"             : post.get("like",{}).get("data",None),
                    "likes_count"       : post.get("like",{}).get("summary",{}).get("total_count",None),
                    "wows"              : post.get("wow", {}).get("data", None),
                    "wows_count"        : post.get("wow", {}).get("summary", {}).get("total_count", None),
                    "sads"              : post.get("sad", {}).get("data", None),
                    "sads_count"        : post.get("sad", {}).get("summary", {}).get("total_count", None),
                    "angrys"            : post.get("angry", {}).get("data", None),
                    "angrys_count"      : post.get("angry", {}).get("summary", {}).get("total_count", None),
                    "loves"             : post.get("love", {}).get("data", None),
                    "loves_count"       : post.get("love", {}).get("summary", {}).get("total_count", None),
                    "hahas"             : post.get("haha", {}).get("data", None),
                    "hahas_count"       : post.get("haha", {}).get("summary", {}).get("total_count", None),
                    "pageinfo"          : temppage,
                    "lang"              : 'en',#sutils.detect_language(message),
                })
        return tempposts

    def is_ascii(self,s):
        """
        Find weather the string is ascii or not , if ascii it will return True else False
        :return: Bool
        """
        return all(ord(c) < 128 for c in s)


    def unicode_decode(self,text):
        """
        Decoding the text from unicode to utf-8
        :param text: unicoded string
        :return: String
        """
        try:
            return text.encode('utf-8').decode()
        except UnicodeDecodeError:
            return text.encode('utf-8')

    def scrapeFacebookPageFeedStatus(self,q):

        base                = "https://graph.facebook.com/v2.9" #Graph Api Url
        node                = "/search?q={}&type=page".format(urllib.quote_plus(q)) # End Point of the Graph Api
        parameters          = "&limit={}&access_token={}".format(5, self.access_token) # included the access_token for url

        pageFields          = "&fields="+self.getpageFileds() # getting the page fields
        reactionFields      = self.getReactionsFields() # Reaction Fields
        postFields          = self.getpostFields().replace('postreactions',reactionFields) # post fields and reaction fields included
        actual_url          = base + node + parameters + pageFields + postFields # Actual url is formed with all fields

        #requesting for the data from Graph API
        #try:
        pages =  json.loads(self.request_until_succeed(actual_url))['data']
        return self.parseResponse(pages)
        #except Exception as e :
        #    print e, "Facebook Utils.."
        #   return []


if __name__ == "__main__":
    futils = FetchFacebookData()
    import time
    starttimr = time.time()
    print json.dumps(futils.scrapeFacebookPageFeedStatus(q="narendramodi"),default=json_util.default)

    print "time taken",time.time() - starttimr
