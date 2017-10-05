
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apsma.settings")

import logging
import MySQLdb
from socialanalytics.utils import refresh_data
from datetime import datetime
import multiprocessing


from django_crontab.crontab import Crontab


def getKeyWords():

    db = MySQLdb.connect(host="10.1.4.57", user="root", passwd="Cosmos12#", db='usermanagement')
    cursor = db.cursor()
    cursor.execute("select keyword from usermanage_keywords where status != 0")
    return [r[0] for r in cursor.fetchall()]

def scheduled_job():

    keywords = getKeyWords()
    print keywords
    for keyword in keywords:
        p1 = multiprocessing.Process(target=refresh_data.load_key_data, args=(keyword ,'news',))
        p1.start()
        p2 = multiprocessing.Process(target=refresh_data.load_key_data, args=(keyword, 'facebook',))
        p2.start()
        p3 = multiprocessing.Process(target=refresh_data.load_key_data, args=(keyword, 'twitter',))
        p3.start()
        p4 = multiprocessing.Process(target=refresh_data.load_key_data, args=(keyword, 'youtube',))
        p4.start()

        print keyword +" data loading in proess...... " + datetime.now().__str__()


def otherjob(x,y):
    print x,y

if __name__ == '__main__':
    scheduled_job()
    #print getKeyWords()