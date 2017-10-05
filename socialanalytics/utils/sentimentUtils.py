# -*- coding: utf-8 -*-
from textblob import TextBlob
from datetime import datetime
from django.utils.encoding import smart_text

colors = ['#e44a00','#f8bd19','#6baa01']

class SentimentUtils(object):

    def unicode_decode(self,text):
        if text:
            return smart_text(text,encoding='utf-8',strings_only=False,errors='strict')
        else:
            return None
        # try:
        #     return text.encode('utf-8').decode()
        # except UnicodeDecodeError:
        #     try:
        #         return text.encode('utf-8')
        #     except:
        #         return str(text)

    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)

    def detect_language(self,word):

        if word is None or len(word) <=2:
            return 'en'
        if not self.is_ascii(word):
            try:
                #print word
                return TextBlob(word).detect_language()
            except:
                return 'en'
        else:
            return 'en'

    def get_sentiment(self, engwrd,language=None):

        if engwrd is not None and len(engwrd ) > 2 :

            blob = TextBlob(engwrd)
            try :
               analysis = blob.translate(from_lang='auto',to='en')
               if analysis.sentiment.polarity > 0.0:
                    return {'text':self.unicode_decode(analysis.__str__()),'polarity': {'key': 'positive','value': analysis.sentiment.polarity,"color":colors[2]}}
               elif analysis.sentiment.polarity == 0.0:
                    return {'text':self.unicode_decode(analysis.__str__()),'polarity': {'key': 'neutral','value' : analysis.sentiment.polarity,"color":colors[1]}}
               else:
                    return {'text':self.unicode_decode(analysis.__str__()),'polarity': {'key': 'negative', 'value' : analysis.sentiment.polarity,"color":colors[0]}}
            except Exception as e :

                analysis = blob

                if analysis.sentiment.polarity >0.0:
                    return {'text':self.unicode_decode(engwrd),'polarity': {'key': 'positive', 'value': analysis.sentiment.polarity, "color": colors[2]}}
                elif analysis.sentiment.polarity ==0.0:
                    return {'text':self.unicode_decode(engwrd),'polarity': {'key': 'neutral', 'value': analysis.sentiment.polarity, "color": colors[1]}}
                else:
                    return {'text':self.unicode_decode(engwrd),'polarity': {'key': 'negative', 'value': analysis.sentiment.polarity, "color": colors[0]}}
        else:
            return {'text':None,'polarity': {'key': 'neutral', 'value': 0.0}}

    def translate(self,source,from_lang='auto',to_lang='en'):

        try:
            blob = TextBlob(source)
            return blob.translate(from_lang=from_lang,to=to_lang)
        except:
            return source

if __name__ =='__main__':
    sutils = SentimentUtils()
    print sutils.get_sentiment("This is the Worst moment in my life")