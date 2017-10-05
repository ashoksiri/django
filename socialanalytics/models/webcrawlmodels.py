from __future__ import unicode_literals
from mongoengine import Document, EmbeddedDocument, fields

from django.db import models
from facebookmodels import Polarity

class News(Document):
    """
        Actual News Document Fetched from RSS Services

        Example:
    {
    "created_at" : ISODate("2017-07-12T13:29:12.000Z"),
    "link" : "http://news.google.com/news/url?sa=t&fd=R&ct2=us&usg=AFQjCNH1G8pzXwdNrMUrs349GhnZY8mvaQ&clid=c3a7d30bb8a4878e06b80cf16b898331&ei=lCdmWYimKpTD8QW3pqeIBA&url=http://economictimes.indiatimes.com/news/economy/policy/ensure-all-traders-register-under-gst-by-aug-15-pm-narendra-modi-to-chief-secretaries/articleshow/59563606.cms",
    "description" : "Ensure all traders register under GST by Aug 15: PM Narendra Modi to Chief Secretaries. By PTI | Jul 12, 2017, 06.58 PM IST. Post a Comment. Untitled-4 GST was rolled out on July 1, ushering a new system of indirect taxes in the country.",
    "image" : "http://t1.gstatic.com/images?q=tbn:ANd9GcTK3yk-7f0LeT7fp_IS00Mm8FQG1jqBLVN6LcmHOtTSbEYaGAXqfJSVvYP-szzVaTdHVxBcsGuN",
    "title" : "Ensure all traders register under GST by Aug 15: PM Narendra Modi to Chief Secretaries - Economic Times",
    "source" : "Economic Times",
    "polarity" : {
        "key" : "negative",
        "value" : "0.136363636364",
        "color" : "#e44a00"
    },
    "searchKey" : "narendramodi",
    "sourceType" : "news",
    "lang" : "en"
}
    """

    newsid = fields.StringField()
    created_at = fields.DateTimeField()
    link = fields.StringField()
    description = fields.StringField()
    description_parsed = fields.StringField()
    image = fields.StringField()
    title = fields.StringField()
    source = fields.StringField()
    polarity = fields.EmbeddedDocumentField(Polarity)
    searchKey = fields.StringField()
    sourceType = fields.StringField(default="news")
    lang  = fields.StringField(default='en')

class NewsEmbedded(EmbeddedDocument):

    newsid = fields.StringField()
    created_at = fields.DateTimeField()
    link = fields.StringField()
    description = fields.StringField()
    description_parsed = fields.StringField()
    image = fields.StringField()
    title = fields.StringField()
    source = fields.StringField()
    polarity = fields.EmbeddedDocumentField(Polarity)
    searchKey = fields.StringField()
    sourceType = fields.StringField(default="news")
    lang  = fields.StringField(default='en')