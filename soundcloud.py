#!/usr/bin/env python3

#import globaux
import requests, time
from bs4 import BeautifulSoup
from urllib.error import HTTPError


def userid_info(url, token):
    #requête web
    req = requests.get(url)
    #parsing html
    datahtml = BeautifulSoup(req.content, "html.parser")
    # récupère l'id
    userid = datahtml.find('meta', property="twitter:app:url:googleplay")['content'].split(':')[-1]

    return userid

def listtracks(userid, token):
    url = f"https://api-v2.soundcloud.com/users/{userid}/tracks?representation=&client_id={token}&limit=20&offset=0&linked_partitioning=1&app_version=1628858614&app_locale=fr"
    #requête web
    reqJson = requests.get(url).json()
    collection = reqJson["collection"]

    return collection


def listcomments(track, token):
    trackid = track['id']
    url = f"https://api-v2.soundcloud.com/tracks/{trackid}/comments?threaded=0&filter_replies=1&client_id={token}&limit=200&offset=0&linked_partitioning=1&app_version=1628858614&app_locale=fr"
    #requête web
    reqJson = requests.get(url).json()
    #parsing html
    collection = reqJson["collection"]

    while(reqJson["next_href"] != None):
        reqJson = requests.get(reqJson["href_url"]).json()
        collection += reqJson["collection"]

    return collection


def metrics_comments(comments):
    dict_user = {}
    for i in comments:
        if(i['user']['id'] in dict_user.keys()):
            dict_user[i['user']['id']]['nb'] += 1
        else:
            dict_user[i['user']['id']] = {'nb' : 1, 'username' : i['user']['username'], "link" : i['user']['permalink_url']}
    #conversion en liste pour le tri :
    dict_user = sorted(dict_user.values(), key=lambda t: t['nb'], reverse=True)
    return dict_user
