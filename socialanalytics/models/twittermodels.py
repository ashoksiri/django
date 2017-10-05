# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *
from socialanalytics.models.facebookmodels import Polarity




class MetaData(EmbeddedDocument):
    """
        Metadata of Tweet
    """
    iso_language_code = StringField(null=True)
    result_type = StringField(null=True)




class Contributor(EmbeddedDocument):
    """
    Deprecated Nullable A collection of brief user objects (usually only one)
    indicating users who contributed to the authorship of the tweet, on behalf of
    the official tweet author. This is a legacy value and is not actively used.

    Example :
    "contributors":
    [
        {
            "id":819797,
            "id_str":"819797",
            "screen_name":"episod"
        }
    ]

    """

    id = IntField(null=True)
    it_str = StringField(null=True)
    screen_name = StringField(null=True)




class Coordinates(EmbeddedDocument):
    """
    Nullable Represents the geographic location of this Tweet as reported by the user or client application.
    The inner coordinates array is formatted as geoJSON (longitude first, then latitude).

    Example:

    "coordinates":
    {
        "coordinates":
        [
            -75.14310264,
            40.05701649
        ],
        "type":"Point"
    }
    """

    coordinates = ListField(null=True)
    type = StringField(null=True)





class UMention(EmbeddedDocument):
    """
    Represents other Twitter users mentioned in the text of the Tweet.
    Example:

    {
      "user_mentions": [
        {
          "name": "Twitter API",
          "indices": [
            4,
            15
          ],
          "screen_name": "twitterapi",
          "id": 6253282,
          "id_str": "6253282"
        }
      ]
    }
    """
    id = IntField(null=True)
    id_str = StringField(null=True)
    name = StringField(null=True)





class HashTag(EmbeddedDocument):
    """
    Represents hashtags which have been parsed out of the Tweet text.

    Example:
    {
      "hashtags": [
        {
          "indices": [
            32,
            36
          ],
          "text": "lol"
        }
      ]
    }
    """
    text = StringField(null=True)





class Size(EmbeddedDocument):
    """
    "sizes":{
            "thumb":{"h":150, "resize":"crop", "w":150},
            "large":{"h":238, "resize":"fit", "w":226},
            "medium":{"h":238, "resize":"fit", "w":226},
            "small":{"h":238, "resize":"fit", "w":226}
            }
    """
    h = IntField(null=True)
    resize = StringField(null=True)
    w = IntField(null=True)





class Url(EmbeddedDocument):
    """
    Represents URLs included in the text of a Tweet or within textual fields of a user object
    Example:
    {
      "urls": [
        {
          "indices": [
            32,
            52
          ],
          "url": "http://t.co/IOwBrTZR",
          "display_url": "youtube.com/watch?v=oHg5SJ…",
          "expanded_url": "http://www.youtube.com/watch?v=oHg5SJYRHA0"
        }
      ]
    }
    """
    url = StringField(null=True)
    display_url = StringField(null=True)
    expanded_url = StringField(null=True)





class Sizes(EmbeddedDocument):
    """
    Sizes of the Media see Size Embedded Document.
    """
    thumb = EmbeddedDocumentField(Size, null=True)
    large = EmbeddedDocumentField(Size, null=True)
    medium = EmbeddedDocumentField(Size, null=True)
    small = EmbeddedDocumentField(Size, null=True)





class Media(EmbeddedDocument):
    """
    Represents media elements uploaded with the Tweet.

    {
      "media": [
        {
          "type": "photo",
          "sizes": {
            "thumb": {
              "h": 150,
              "resize": "crop",
              "w": 150
            },
            "large": {
              "h": 238,
              "resize": "fit",
              "w": 226
            },
            "medium": {
              "h": 238,
              "resize": "fit",
              "w": 226
            },
            "small": {
              "h": 238,
              "resize": "fit",
              "w": 226
            }
          },
          "indices": [
            15,
            35
          ],
          "url": "http://t.co/rJC5Pxsu",
          "media_url": "http://p.twimg.com/AZVLmp-CIAAbkyy.jpg",
          "display_url": "pic.twitter.com/rJC5Pxsu",
          "id": 114080493040967680,
          "id_str": "114080493040967680",
          "expanded_url": "http://twitter.com/yunorno/status/114080493036773378/photo/1",
          "media_url_https": "https://p.twimg.com/AZVLmp-CIAAbkyy.jpg"
        }
      ]
    }
    """
    type = StringField()
    sizes = EmbeddedDocumentField(Sizes, null=True)
    url = StringField(null=True)
    media_url = StringField()
    display_url = StringField()
    id = IntField()
    id_str = StringField()
    expanded_url = StringField()
    media_url_https = StringField()





class BoundBox(EmbeddedDocument):
    """
    Attribute from Place
    Example:

    "bounding_box":
        {
            "coordinates":
            [[
                    [-77.119759,38.791645],
                    [-76.909393,38.791645],
                    [-76.909393,38.995548],
                    [-77.119759,38.995548]
            ]],
            "type":"Polygon"
        }
    """
    type = StringField()
    coordinates = ListField()




class Entity(EmbeddedDocument):
    """
    Entities which have been parsed out of the text of the Tweet.

    Example:
    "entities":
    {
        "hashtags":[],
        "urls":[],
        "user_mentions":[]
    }
    """

    symbols = ListField(null=True)
    user_mentions = EmbeddedDocumentListField(UMention, null=True)
    hashtags = EmbeddedDocumentListField(HashTag, null=True)
    media = EmbeddedDocumentListField(Media, null=True)
    url = EmbeddedDocumentListField(Url, null=True)





class Place(EmbeddedDocument):
    """
    Nullable When present, indicates that the tweet is associated (but not necessarily originating from) a Place .

    Example:

    "place":
    {
        "attributes":{},
         "bounding_box":
        {
            "coordinates":
            [[
                    [-77.119759,38.791645],
                    [-76.909393,38.791645],
                    [-76.909393,38.995548],
                    [-77.119759,38.995548]
            ]],
            "type":"Polygon"
        },
         "country":"United States",
         "country_code":"US",
         "full_name":"Washington, DC",
         "id":"01fbe706f872cb32",
         "name":"Washington",
         "place_type":"city",
         "url": "http://api.twitter.com/1/geo/id/01fbe706f872cb32.json"
    }
    """
    full_name = StringField()
    url = StringField()
    country = StringField()
    place_type = StringField()
    bounding_box = EmbeddedDocumentField(BoundBox, null=True)
    contained_within = ListField()
    attributes = DictField()
    id = StringField()
    name = StringField()





class EUrl(EmbeddedDocument):
    '''
        Entity Urls Attribute
    '''
    urls = EmbeddedDocumentListField(Url, null=True)





class UEntity(EmbeddedDocument):
    '''
        Entities which have been parsed out of the url or description fields defined by the user. Read more about User Entities .

        Example:
    "entities": {
      "url": {
        "urls": [
          {
            "url": "http://dev.twitter.com",
            "expanded_url": null,
            "indices": [0, 22]
          }
        ]
      },
      "description": {"urls":[] }
    }
    '''
    url = EmbeddedDocumentField(EUrl, null=True)
    description = EmbeddedDocumentField(EUrl, null=True)





class TUser(EmbeddedDocument):
    """
    The user who posted this Tweet. Perspectival attributes embedded within this object are unreliable.
    Example:
    {
      "user": {
        "statuses_count": 3080,
        "favourites_count": 22,
        "protected": false,
        "profile_text_color": "437792",
        "profile_image_url": "...",
        "name": "Twitter API",
        "profile_sidebar_fill_color": "a9d9f1",
        "listed_count": 9252,
        "following": true,
        "profile_background_tile": false,
        "utc_offset": -28800,
        "description": "The Real Twitter API. I tweet about API changes. Don't get an answer? It's on my website.",
        "location": "San Francisco, CA",
        "contributors_enabled": true,
        "verified": true,
        "profile_link_color": "0094C2",
        "followers_count": 665829,
        "url": "http://dev.twitter.com",
        "default_profile": false,
        "profile_sidebar_border_color": "0094C2",
        "screen_name": "twitterapi",
        "default_profile_image": false,
        "notifications": false,
        "display_url": null,
        "show_all_inline_media": false,
        "geo_enabled": true,
        "profile_use_background_image": true,
        "friends_count": 32,
        "id_str": "6253282",
        "entities": {
          "hashtags": [],
          "urls": [],
          "user_mentions": []
        },
        "expanded_url": null,
        "is_translator": false,
        "lang": "en",
        "time_zone": "Pacific Time (US & Canada)",
        "created_at": "Wed May 23 06:01:13 +0000 2007",
        "profile_background_color": "e8f2f7",
        "id": 6253282,
        "follow_request_sent": false,
        "profile_background_image_url_https": "...",
        "profile_background_image_url": "..."
      }
    }
    """
    follow_request_sent = BooleanField(default=False)
    has_extended_profile = BooleanField(default=False)
    profile_use_background_image = BooleanField(default=False)
    default_profile_image = BooleanField(default=False)
    id = IntField()
    id_str = StringField()
    profile_background_image_url_https = StringField(null=True)
    verified = BooleanField(default=False)
    translator_type = StringField(null=True)
    profile_text_color = StringField(null=True)
    profile_image_url_https = StringField(null=True)
    profile_sidebar_fill_color = StringField(null=True)
    followers_count = IntField()
    profile_sidebar_border_color = StringField()
    profile_background_color = StringField()
    listed_count = IntField()
    is_translation_enabled = BooleanField(default=False)
    utc_offset = IntField(null=True)
    statuses_count = IntField(null=True)
    description = StringField(null=True)
    friends_count = IntField()
    location = StringField(null=True)
    profile_link_color = StringField(null=True)
    profile_image_url = StringField(null=True)
    following = BooleanField(default=False)
    geo_enabled = BooleanField(default=False)
    profile_banner_url = StringField(null=True)
    profile_background_image_url = StringField(null=True)
    screen_name = StringField()
    lang = StringField()
    profile_background_tile = BooleanField(default=False)
    favourites_count = IntField()
    name = StringField()
    notifications = BooleanField(default=False)
    url = StringField(null=True)
    created_at = DateTimeField(null=True)
    contributors_enabled = BooleanField(default=False)
    time_zone = StringField(null=True)
    protected = BooleanField(default=False)
    default_profile = BooleanField(default=False)
    is_translator = BooleanField(default=False)
    entities = EmbeddedDocumentField(UEntity, null=True)




class TweetEMB(EmbeddedDocument):
    """
    Tweet Object Embedded
    """
    contributors = EmbeddedDocumentListField(Contributor, null=True)
    truncated = BooleanField(default=False)
    text = StringField(null=True)
    text_parsed = StringField(null=True)
    is_quote_status = BooleanField(default=False)
    in_reply_to_status_id = IntField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    id = IntField()
    id_str = StringField()
    favorite_count = IntField()
    retweeted = BooleanField(default=False)
    coordinates = EmbeddedDocumentField(Coordinates, null=True)
    source = StringField()
    in_reply_to_screen_name = StringField(null=True)
    in_reply_to_user_id = IntField(null=True)
    retweet_count = IntField()
    favorited = BooleanField(default=False)
    in_reply_to_user_id_str = StringField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    lang = StringField()
    created_at = DateTimeField()
    place = EmbeddedDocumentField(Place, null=True)
    entities = EmbeddedDocumentField(Entity, null=True)
    user = EmbeddedDocumentField(TUser,null=True)
    metadata = EmbeddedDocumentField(MetaData, null=True)




class TweetEmbedded(EmbeddedDocument):
    """
        Tweet Object Embedded
    """
    contributors = EmbeddedDocumentListField(Contributor, null=True, default=[])
    truncated = BooleanField(default=False)
    text = StringField(null=True)
    text_parsed = StringField(null=True)
    is_quote_status = BooleanField(default=False)
    in_reply_to_status_id = IntField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    tweetid = IntField(unique=True)
    id_str = StringField()
    favorite_count = IntField()
    retweeted = BooleanField(default=False)
    coordinates = EmbeddedDocumentField(Coordinates, null=True)
    source = StringField()
    in_reply_to_screen_name = StringField(null=True)
    in_reply_to_user_id = IntField(null=True)
    retweet_count = IntField()
    retweeted_status = EmbeddedDocumentField(TweetEMB, null=True)
    favorited = BooleanField(default=False)
    in_reply_to_user_id_str = StringField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    lang = StringField()
    created_at = DateTimeField()
    place = EmbeddedDocumentField(Place, null=True)
    entities = EmbeddedDocumentField(Entity, null=True)
    user = EmbeddedDocumentField(TUser)
    metadata = EmbeddedDocumentField(MetaData, null=True)
    polarity = EmbeddedDocumentField(Polarity, null=True)
    searchKey = StringField()
    sourceType = StringField(default='twitter')




class Tweet(Document):
    """
    Tweet Object Original

    """
    contributors = EmbeddedDocumentListField(Contributor, null=True, default=[])
    truncated = BooleanField(default=False)
    text = StringField(null=True)
    text_parsed = StringField(null=True)
    is_quote_status = BooleanField(default=False)
    in_reply_to_status_id = IntField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    tweetid = IntField()
    id_str = StringField()
    favorite_count = IntField()
    retweeted = BooleanField(default=False)
    coordinates = EmbeddedDocumentField(Coordinates, null=True)
    source = StringField()
    in_reply_to_screen_name = StringField(null=True)
    in_reply_to_user_id = IntField(null=True)
    retweet_count = IntField()
    retweeted_status = EmbeddedDocumentField(TweetEMB, null=True)
    favorited = BooleanField(default=False)
    in_reply_to_user_id_str = StringField(null=True)
    in_reply_to_status_id_str = StringField(null=True)
    lang = StringField()
    created_at = DateTimeField()
    place = EmbeddedDocumentField(Place, null=True)
    entities = EmbeddedDocumentField(Entity, null=True)
    user = EmbeddedDocumentField(TUser)
    metadata = EmbeddedDocumentField(MetaData, null=True)
    polarity = EmbeddedDocumentField(Polarity, null=True)
    searchKey = StringField()
    sourceType = StringField(default='twitter')



class TweetGis(Document):
    """
        Tweet With Gis Fields
    """
    user_id             = StringField(null=True)
    user_name           = StringField(null=True)
    user_screen_name    = StringField(null=True)
    created_date        = StringField(null=True)
    created_time        = StringField(null=True)
    tweet_id            = StringField(null=True)
    text                = StringField(null=True)
    text_parsed         = StringField(null=True)
    latitude            = FloatField(null=True)
    longitude           = FloatField(null=True)
    user_following      = IntField(null=True)
    user_followers      = IntField(null=True)
    total_tweets        = IntField(null=True)
    tweet_location      = StringField(null=True)
    tweet_location_type = StringField(null=True)
    tweet_country       = StringField(null=True)
    profile_location    = StringField(null=True)
    profile_image_url   = StringField(null=True)
    profile_url         = StringField(null=True)



