# from lxml import etree
# from sentimentUtils import SentimentUtils
# import hashlib,urllib2
# from multiprocessing import Process, Manager
# from bson import json_util
# from bs4 import BeautifulSoup
# from dateutil.parser import *
# import dateparser,urllib,time,links,grequests
# from urllib2 import urlopen, Request
# import xml.etree.ElementTree as ET
#
# sutils = SentimentUtils()
# info = dateparser.parserinfo()
# parser = etree.XMLParser(strip_cdata=False)
#
# def request_until_succeed(url):
#     req = Request(url)
#     success = False
#     while success is False:
#         try:
#             response = urlopen(req)
#             if response.getcode() == 200:
#                 success = True
#         except Exception as e:
#             print(e)
#             time.sleep(5)
#
#             # print("Error for URL {}: {}".format(url, datetime.datetime.now()))
#             print("Retrying.")
#
#     return response.read()
#
# def getNews(q):
#     news = []
#
#     if q is None or q == '':
#         return {}
#     else:
#         url = 'https://news.google.com/news?hl=en&tab=nn&edchanged=1&authuser=0&ned=en_in&output=rss&q=' + urllib2.quote(q)
#         xml = request_until_succeed(url)
#         doc = ET.fromstring(xml)
#
#         for d in doc.findall("./channel/item"):
#             try:
#                 b = BeautifulSoup(d.find("./description").text, features="html.parser")
#                 imagetd = b.find("table").find("tr").findAll("td")[0]
#                 descriptiontd = b.find("table").find("tr").findAll("td")[1]
#                 # print d.find("./title").text
#                 title = ((d.find("./title").text).encode('utf-8'))
#                 # print title
#                 news.append({
#                     "newsid": hashlib.md5(title).hexdigest(),
#                     "title": title,
#                     "link": d.find("./link").text,
#                     "created_at": parse(d.find("./pubDate").text),
#                     "image": "http:" + imagetd.find("img").get("src") if imagetd.find("img") is not None else 'NA    ',
#                     "source": descriptiontd.findAll("font")[2].text,
#                     "description": descriptiontd.findAll("font")[3].text,
#                     "polarity": sutils.get_sentiment(descriptiontd.findAll("font")[3].text)
#                 })
#             except:
#                 pass
#     return news
#
# def eenadurss(q):
#
#     news = []
#     rs = (grequests.get(u) for u in links.EENADULINKS)
#     data =[d for d in grequests.map(rs) if d is not None]
#
#     for d in data:
#
#         try:
#             doc = etree.fromstring(d.text.encode('utf-8'))
#
#             for item in doc.findall('./channel/item'):
#                 title = item.find('./title').text
#                 if q.lower() in title.lower():
#                     newsid = hashlib.md5(title.encode('utf-8')).hexdigest
#                     guid = item.find('./guid').text
#                     author = item.find('./author').text
#                     pubdate = parse(item.find('./pubDate').text,parserinfo=info)
#                     desc =  item.find('./description').text
#                     image =  item.find('./image') if item.find('./image') else 'NA'
#                     polarity = sutils.get_sentiment(desc)
#                     news.append({"newsid" : newsid,
#                                  "title": title,
#                                  'link' : guid,
#                                  "author": author,
#                                  "created_at" : pubdate,
#                                  'source' : 'EENADU',
#                                  "description" : desc,
#                                  "image": image,
#                                  "polarity":polarity})
#         except Exception as e:
#            #print e.message
#            pass
#
#     return news
#
# def apherald(q):
#     news = []
#     rs = (grequests.get(u) for u in links.APHERALDLINKS)
#     data = grequests.map(rs)
#     data = [d for d in data if d is not None]
#
#     for d in data :
#         try:
#             d = d.text.encode('utf-8')
#             d = d[d.index('<'):len(d)]
#             doc = etree.fromstring(d)
#
#             for item in doc.findall('./channel/item'):
#                 title = item.find('./title').text
#                 if q.lower() in title.lower():
#
#                     newsid = hashlib.md5(title.encode('utf-8')).hexdigest()
#                     guid = item.find('./guid').text
#                     pubdate = parse(item.find('./pubDate').text, parserinfo=info)
#                     image = item.find('./image').text
#                     desc   = '<description>'+item.find('./description').text+'</description>'
#                     desc = etree.XML(desc,parser=etree.XMLParser(strip_cdata=True))
#                     b = BeautifulSoup(desc.text,features='html.parser')
#                     desc = b.text
#                     polarity = sutils.get_sentiment(desc)
#
#                     news.append({"newsid": newsid,
#                                  'title' : title,
#                                  'source' : "Ap Herald",
#                                  "link": guid,
#                                  "created_at": pubdate,
#                                  "description": desc,
#                                  "image": image,
#                                  "polarity": polarity})
#         except Exception as e:
#             print e.message
#             pass
#     return news
#
# def hindurss(q):
#     news = []
#     rs = (grequests.get(u) for u in links.HINDULINKS)
#     data = grequests.map(rs)
#     data = [d for d in data if d is not None]
#     for d in data:
#         try:
#             d = d.text.encode('utf-8')
#             d = d[d.index('<'):len(d)]
#             doc = etree.fromstring(d)
#
#             for item in doc.findall('./channel/item'):
#                 title = item.find('./title').text
#                 if q.lower() in title.lower():
#                     newsid = hashlib.md5(title.encode('utf-8')).hexdigest()
#                     guid = item.find('./guid').text
#                     pubdate = parse(item.find('./pubDate').text, parserinfo=info)
#                     desc = '<description>' + item.find('./description').text + '</description>'
#                     desc = etree.XML(desc, parser=etree.XMLParser(strip_cdata=True))
#                     b = BeautifulSoup(desc.text, features='html.parser')
#                     desc = b.text
#                     polarity = sutils.get_sentiment(desc)
#
#                     news.append({"newsid": newsid,
#                                  'title' : title,
#                                  'link' : guid,
#                                  "source": 'The Hindu',
#                                  "created_at": pubdate,
#                                  "description": desc,
#                                  "image": 'NA',
#                                  "polarity": polarity})
#         except Exception as e:
#             print e.message
#             pass
#     return news
#
# def oneindiarss(q):
#     news = []
#     rs = (grequests.get(u) for u in links.ONEINDIALINKS)
#     data = grequests.map(rs)
#     data = [d for d in data if d is not None]
#     for d in data:
#         try:
#             d = d.text.encode('utf-8')
#             d = d[d.index('<'):len(d)]
#             doc = etree.fromstring(d)
#
#             for item in doc.findall('./channel/item'):
#                 title = item.find('./title').text
#                 if q.lower() in title.lower():
#                     newsid = hashlib.md5(title.encode('utf-8')).hexdigest()
#                     guid = item.find('./guid').text
#                     pubdate = parse(item.find('./pubDate').text, parserinfo=info)
#                     desc = '<description>' + item.find('./description').text + '</description>'
#                     desc = etree.XML(desc, parser=etree.XMLParser(strip_cdata=True))
#                     b = BeautifulSoup(desc.text, features='html.parser')
#                     desc = b.text
#                     polarity = sutils.get_sentiment(desc)
#
#                     news.append({"newsid": newsid,
#                                  'title' : title,
#                                  "author": 'One India',
#                                  'link' : guid,
#                                  "created_at": pubdate,
#                                  "description": desc,
#                                  "image": 'NA',
#                                  "polarity": polarity})
#         except Exception as e:
#             print e.message
#             pass
#     return news
#
#
# def getNews(keyword):
#
#     data = getNews(keyword) \
#            + oneindiarss(keyword) \
#            + hindurss(keyword) \
#            + eenadurss(keyword) + \
#            apherald(keyword)
#     return data
#
# if __name__ == "__main__":
#
#
#     starttime = time.time()
#
#     print "Time Taken ", time.time() - starttime, "Seconds"
#    # print json.dumps(newss,indent=2,default=json_util.default)