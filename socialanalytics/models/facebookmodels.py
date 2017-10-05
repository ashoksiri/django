# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import Document,EmbeddedDocument, fields
from django.db import models

# Create your models here.

def convertPolarityDict(polarity):
    return {"key": polarity.get('key'),
            "value": polarity.get('value'),
            "color": polarity.get('color'),
            }

class Polarity(EmbeddedDocument):
    """
        polarity Object contains key as positive or negative or neutral

    """
    key   = fields.StringField(null=True)
    value = fields.FloatField(null=True)
    color = fields.StringField(null=True)

    def __dict__(self):
        return {"key": self.key,
                "value": self.value,
                "color": self.color,
                }

class Location(EmbeddedDocument):
    """
        Location object Mapping to post location if user mentioned Location in the post

    """
    city    = fields.StringField(null=True)
    city_id = fields.StringField(null=True)
    country = fields.StringField(null=True)
    country_code = fields.StringField(null=True)
    latitude = fields.StringField(null=True)
    located_in = fields.StringField(null=True)
    longitude = fields.StringField(null=True)
    name = fields.StringField(null=True)
    region = fields.StringField(null=True)
    region_id = fields.StringField(null=True)
    state = fields.StringField(null=True)
    street = fields.StringField(null=True)
    zip = fields.StringField(null=True)

class FacebookPage(EmbeddedDocument):

    """
        Facebook page Details having below fields

        Example:
            "pageinfo" : {
        "category" : "Political Organization",
        "website" : "http://www.narendramodi.in/",
        "about" : "Prime Minister of India",
        "pageid" : "1673710289594030",
        "description" : "Prime Minister of India Narendra Modi’s journey began in the town of Vadnagar in",
        "fan_count" : "192",
        "were_here_count" : "0",
        "talking_about_count" : "89",
        "location" : {
            "city" : "New Delhi",
            "city_id" : "None",
            "country" : "India",
            "latitude" : "None",
            "located_in" : "None",
            "longitude" : "None",
            "region_id" : "None",
            "street" : "Vadnagar",
            "zip" : "384355"
        },
        "name" : "Narendramodi",
        "rating_count" : "0",
        "link" : "https://www.facebook.com/Narendramodi-1673710289594030/",
        "current_location" : {},
        "description_html" : "Prime Minister of India Narendra Modi’s journey began in the town of Vadnagar in"
    }

    """
    category        = fields.StringField(null=True)
    website         = fields.StringField(null=True)
    about           = fields.StringField(null=True)
    pageid          = fields.StringField(null=True)
    description     = fields.StringField(null=True)
    fan_count       = fields.IntField(null=True)
    bio             = fields.StringField(null=True)
    were_here_count = fields.IntField(null=True)
    company_overview= fields.StringField(null=True)
    new_like_count  = fields.IntField(null=True)
    talking_about_count = fields.IntField(null=True)
    location    = fields.EmbeddedDocumentField(Location,null=True)
    name        = fields.StringField(null=True)
    phone       = fields.StringField(null=True)
    contact_address = fields.StringField(null=True)
    rating_count    = fields.IntField(null=True)
    link        = fields.StringField(null=True)
    current_location    = fields.StringField(null=True)
    general_info        = fields.StringField(null=True)
    description_html    = fields.StringField(null=True)


class FbComment(EmbeddedDocument):
     """
        Facebook comment field embedded in facebook post
        "comments" : [
        {
            "from_id" : "275461592921596",
            "from_user" : "Gopal Jee Singh",
            "created_time" : ISODate("2017-05-11T09:09:41.000Z"),
            "message" : "सराहनीय कार्य।"
        },
        {
            "from_id" : "275461592921596",
            "from_user" : "Gopal Jee Singh",
            "created_time" : ISODate("2017-05-19T09:11:46.000Z"),
            "message" : "Apriciatted"
        }
    ]
     """

     commentid      = fields.StringField(null=True)
     from_id        = fields.StringField(null=True)
     from_user      = fields.StringField(null=True)
     created_time   = fields.DateTimeField(null=True)
     message        = fields.StringField(null=True)
     message_parsed = fields.StringField(null=True)
     polarity       = fields.EmbeddedDocumentField(Polarity,null=True)



     def __dict__(self):
         return {"commentid" :self.commentid,"from_id":self.from_id,
                 "from_user":self.from_user,"created_time":self.created_time,
                 "message":self.message,"message_parsed":self.message_parsed,
                 "polarity":self.polarity.__dict__()}

     def __hash__(self):
         return hash(id)

class FbReaction(EmbeddedDocument):
    """
        facebook post reaction enbedded in the post like LIKE,WOW,HAHA,ANGRY,SAD,LOVE

        Example:
            "likes" : [
        {
            "name" : "Zxz Zxz Suman",
            "id" : "337165666696652"
        },
        {
            "name" : "Sandip Kadam",
            "id" : "198538044010393"
        },
        {
            "name" : "Rajveer Ilavish Jatt",
            "id" : "1883333718656969"
        }]
    """
    id = fields.StringField(null=True)
    name = fields.StringField(null=True)



class FacebookPostEmbedded(EmbeddedDocument):
    """
        Actual facebook post from Facebook
    """
    postid        = fields.StringField(null=True)
    type          = fields.StringField(null=True)
    message       = fields.StringField(null=True)
    message_parsed = fields.StringField(null=True)
    created_time  = fields.DateTimeField(null=True)#StringField(null=True)
    place         = fields.EmbeddedDocumentField(Location,null=True)
    permalink_url = fields.StringField(null=True)
    link          = fields.StringField(null=True)
    picture       = fields.StringField(null=True)
    shares        = fields.IntField(null=True,default=0)
    comment_count = fields.IntField(null=True,default=0)
    likes_count   = fields.IntField(null=True,default=0)
    wows_count    = fields.IntField(null=True,default=0)
    hahas_count   = fields.IntField(null=True,default=0)
    angrys_count  = fields.IntField(null=True,default=0)
    sads_count    = fields.IntField(null=True,default=0)
    loves_count   = fields.IntField(null=True,default=0)
    updated_time  = fields.DateTimeField(null=True)
    likes         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    wows          = fields.EmbeddedDocumentListField(FbReaction,null=True)
    loves         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    hahas         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    sads          = fields.EmbeddedDocumentListField(FbReaction,null=True)
    angrys        = fields.EmbeddedDocumentListField(FbReaction,null=True)
    comments      = fields.EmbeddedDocumentListField(FbComment,null=True)
    pageinfo      = fields.EmbeddedDocumentField(FacebookPage,null=True)
    polarity      = fields.EmbeddedDocumentField(Polarity,null=True)
    searchKey     = fields.StringField(null=True)
    sourceType    = fields.StringField(default="facebook")
    lang          = fields.StringField(default='en')

class Facebook(Document):
    """
            Actual facebook post from Facebook
    """
    postid        = fields.StringField(null=True)
    type          = fields.StringField(null=True)
    message       = fields.StringField(null=True)
    message_parsed = fields.StringField(null=True)
    created_time  = fields.DateTimeField(null=True)#StringField(null=True)
    place         = fields.EmbeddedDocumentField(Location,null=True)
    permalink_url = fields.StringField(null=True)
    link          = fields.StringField(null=True)
    picture       = fields.StringField(null=True)
    shares        = fields.IntField(null=True,deafult=0)
    comment_count = fields.IntField(null=True, default=0)
    likes_count   = fields.IntField(null=True, default=0)
    wows_count    = fields.IntField(null=True, default=0)
    hahas_count   = fields.IntField(null=True, default=0)
    angrys_count  = fields.IntField(null=True, default=0)
    sads_count    = fields.IntField(null=True, default=0)
    loves_count   = fields.IntField(null=True, default=0)
    updated_time  = fields.DateTimeField(null=True)
    likes         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    wows          = fields.EmbeddedDocumentListField(FbReaction,null=True)
    loves         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    hahas         = fields.EmbeddedDocumentListField(FbReaction,null=True)
    sads          = fields.EmbeddedDocumentListField(FbReaction,null=True)
    angrys        = fields.EmbeddedDocumentListField(FbReaction,null=True)
    comments      = fields.EmbeddedDocumentListField(FbComment,null=True)
    pageinfo      = fields.EmbeddedDocumentField(FacebookPage,null=True)
    polarity      = fields.EmbeddedDocumentField(Polarity,null=True)
    searchKey     = fields.StringField(null=True)
    sourceType    = fields.StringField(default="facebook")
    lang          = fields.StringField(default='en')