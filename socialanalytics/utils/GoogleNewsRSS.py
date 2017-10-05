"""
    This util package will get the news as RSS from the google new api matched with searchkey.

"""

import urllib2
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
from sentimentUtils import SentimentUtils
import hashlib
from dateutil.parser import *


sutils = SentimentUtils()

def getNews(q):

    news = []

    if q is None or q == '':
        return {}
    else:
        url = 'https://news.google.com/news?hl=en&tab=nn&edchanged=1&authuser=0&ned=en_in&output=rss&q='+urllib2.quote(q)

        xml = requests.get(url)
        doc = ET.fromstring(xml.text.encode("utf-8"))

        for d in doc.findall("./channel/item"):
            try:
                b = BeautifulSoup(d.find("./description").text, features="html.parser")
                imagetd = b.find("table").find("tr").findAll("td")[0]
                descriptiontd = b.find("table").find("tr").findAll("td")[1]
                description  = descriptiontd.findAll("font")[3].text
                polarity  = sutils.get_sentiment(description)
                title= ((d.find("./title").text).encode('utf-8'))
                #print title
                news.append({
                    "newsid"        : hashlib.md5(title).hexdigest(),
                    "title"         : sutils.unicode_decode(title),
                    "link"          : d.find("./link").text,
                    "created_at"    : parse(d.find("./pubDate").text),
                    "image"         : "http:"+imagetd.find("img").get("src") if imagetd.find("img") is not None else 'NA    ',
                    "source"        : descriptiontd.findAll("font")[2].text,
                    "description"   : description,
                    "description_parsed" : polarity.get('text'),
                    "polarity"      : polarity.get('polarity')
                    })
            except:
                pass
    return news

if __name__ == "__main__":
    newss = getNews("rahul gandhi")
    print len(newss)
    # for news in newss:
    #     print json.dumps(news,indent=2,default=json_util.default)