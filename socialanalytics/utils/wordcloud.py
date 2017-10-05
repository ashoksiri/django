
import topicutil
from django.core.cache import cache
import time,os
from collections import Counter
from django.utils.encoding import smart_text
import re
regex = "(@[A-Za-z0-9]+)|([^0-9A-Za-z\'\"\,\. \t])|(\w+:\/\/\S+)"

current_path = os.path.abspath(os.path.dirname(__file__))

def readwords( filename ):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words

positive = readwords(current_path+'/positive-words.txt')
negative = readwords(current_path+'/negative-words.txt')

def getPolarity(q, from_date=None, to_date=None):

        data = topicutil.getdescriptions(searchKey=q,from_date=from_date,to_date=to_date)
        descriptions = [ d.keys() for d in data]
        description = ' '.join([val for sublist in descriptions for val in sublist])

        count = Counter(description.split())
        posword = []
        negword = []
        for key, val in count.iteritems():
            key = key.rstrip('.,?!\n')  # removing possible punctuation signs
            if key in positive:
                posword.append({'key':key,'count':val})
            if key in negative:
                negword.append({'key':key,'count':val})
        result = {}
        result['positive'] = posword
        result['negative'] = negword
        cache.set(q+'_wordcloud',result)
        return result

def getWordCloud(data):
    data = ' '.join(re.sub(regex, " ", data).split())
    data = smart_text(data, encoding='utf-8', strings_only=False, errors='strict')
    count = Counter(data.split())
    posword = []
    negword = []

    for key, val in count.iteritems():
        key = str(key.rstrip('.,?!\n'))  # removing possible punctuation signs
        if key in positive:
            posword.append({'key': key, 'count': val})
        if key in negative:
            negword.append({'key': key, 'count': val})
    result = {}
    result['positive'] = posword
    result['negative'] = negword

    return result

if __name__ == '__main__':
    starttime = time.time()

    print getPolarity(q='narendramodi',from_date='2017-07-01',to_date='2017-08-31')

    print starttime - time.time() , "Seconds"