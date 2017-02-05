'''
Check proxies and insert them into MongoDB
'''

import requests
import re
import pymongo
import time

def checkproxy(pros, link):
    '''select proxies in pros which can reach link '''
    good_proxy = []

    for po in pros:
        try:
            r = requests.get(link,proxies=po,timeout = 3)
            if r.ok:
                good_proxy.append(po)
        except:
            pass
    return good_proxy

def proxyinmongo(mongoaddr,mongoport,dbname,collectioname,proxy_list,links):
    '''Store proxies in MongoDB '''
    client = pymongo.MongoClient(host=mongoaddr, port=mongoport)
    db = client[dbname]

    link_chain = {}

    for link in links:
        reach_proxy = checkproxy(proxy_list,link)
        print link
        print reach_proxy
        for proxy in reach_proxy:
            db[collectioname].insert_one({'destination':link,
                                          'proxy':proxy,
                                          'createdate':time.time()})

if __name__ == '__main__':
    ''' Example '''
    from cnproxies import get_cnproxies
    proxy_list = get_cnproxies()
    links = ['https://www.google.com/']
    proxyinmongo('127.0.0.1',27017,'proxies','google_proxy',proxy_list,links)
