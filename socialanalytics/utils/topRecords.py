
import filtermodels
import mongoengine
from socialanalytics.models.twittermodels import Tweet
from socialanalytics.models.webcrawlmodels import News
from socialanalytics.models.youtubemodels import Video
from collections import Counter
from sentimentUtils import SentimentUtils
from wordcloud import getWordCloud,readwords
from topicutil import regex
import json
from bson import json_util

sutils = SentimentUtils()

db = mongoengine.connect(db='db_apsma',host='10.1.11.23')
#print Video.objects.all()
#tweets = [tweet for tweet in Tweet.objects.aggregate(*pipeline)]

def countPolarity(data):
    positive,negative,neutral = 0,0,0
    for d in data:
        if d.get('key') == 'positive':
            positive = positive+1
        if d.get('key') == 'negative':
            negative = negative+1
        if d.get('key') == 'neutral':
            neutral = neutral+1
    return {'positive':positive,'negative':negative,'neutral':neutral}



def getTweetsFilters(tweets):


    tweetList = []
    hashtags = []
    id = [0]
    polarity = {"negative" : 0,"positive":0,"neutral":0}

    for tweet in tweets:
        #tweet['polarity'] = tweet.get('polarity')
        pol = tweet.get('polarity')
        if pol.get('key') == 'positive':
            polarity['positive'] = polarity['positive'] +1
        if pol.get('key') == 'negative':
            polarity['negative'] = polarity['negative'] + 1
        if pol.get('key') == 'neutral':
            polarity['neutral'] = polarity['neutral'] + 1
        tweetList.append(tweet)
        id.append(tweet['tweetid'])

        for k,v in tweet.get('entities').items():
            if k == 'hashtags':
                hashtags = hashtags+[x.get('text') for x in v]

    tweetList = [t for t in tweetList if t['tweetid'] in set(id)]

    retweets = sorted(set([(status['retweet_count'], status['retweeted_status']['user']['screen_name'],
                            status['retweeted_status']['user']['id_str'], status['text_parsed'])
                           for status in tweets if status.get('retweeted_status').get('user') is not None]), reverse=True)[:20]

    retweets = [{"retweet_count": tweet[0], "user_screenname": tweet[1], 'user_id': tweet[2], 'text': tweet[3]} for
                tweet in retweets]

    import stopwords

    words = Counter(
        [x for x in (' '.join([(status['text_parsed']) for status in tweets]).split()) if x not in stopwords.stop_w])
    words = sorted([{'key': word, 'frequency': words[word]} for word in words], key=lambda x: x['frequency'],
                   reverse=True)[:30]

    users = Counter(
        [(status['user']['name'], status['user']['screen_name'], status['user']['id_str']) for status in tweets])
    users = [{'username': user[0], 'user_screenname': user[1], 'user_id': user[2], 'frequency': user[3]} for user in
             [(user + (users[user],)) for user in users]]
    users = sorted(users, key=lambda x: x['frequency'], reverse=True)[:30]

    popular_words = Counter(hashtags)

    popular_words_list = sorted(
        [({'key':sutils.unicode_decode(x), 'frequency': popular_words[x]}) for x in popular_words],
        key=lambda x: x['frequency'], reverse=True)[:20]

    return   {'tweets': tweetList, 'retweets': retweets,
              'words': words,     'hashtags': popular_words_list,
              'topusers': users   ,'polarity':polarity}


def getNewsFiltered(news):
    print news
    import re
    polarityList = [n.get('polarity') for n in news]
    words = readwords('./positive-words.txt')
    print words
    descriptions = [d.get('description').decode('utf-8') for d in news]
    print descriptions
    description = ' '.join([val for sublist in descriptions for val in sublist.split()])
    count = Counter(description)
    print count
    # for n in news:
    #      n.get('description')
    #description  = ' '.join([n.get('description') for b in news])

    #sentiment =  countPolarity(polarityList)
    #wordcloud = getWordCloud(description)
    #print wordcloud
    #print len(news)


# def getpostsFilters(posts):
#
#     print posts

#if __name__ =='__main__':
   #print  getTweetsFilters(tweets)
   #getNewsFiltered(news=news)