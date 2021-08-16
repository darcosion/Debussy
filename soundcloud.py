#!/usr/bin/env python3

#import globaux
import requests, time, re
from bs4 import BeautifulSoup
from urllib.error import HTTPError


def userid_info(url):
    #requête web
    req = requests.get(url)
    #parsing html
    datahtml = BeautifulSoup(req.content, "html.parser")
    # récupère l'id
    userid = datahtml.find('meta', property="twitter:app:url:googleplay")['content'].split(':')[-1]
    # liste les lib JS
    listlibjs = list(datahtml.findAll('script', crossorigin=""))
    listlibjs.reverse()
    client_id = None
    for i in listlibjs:
        if(not i.has_attr('src')):
            continue
        try:
            reqJS = requests.get(i['src'])
            contentJS = reqJS.content
            if(type(reqJS.content) is bytes):
                contentJS = reqJS.content.decode("utf-8")
            regex = re.search(r"client_id\:\"[aA-zZ0-9]*\"", contentJS)
            if(regex):
                client_id = regex.group(0)[11:-1]
                break
        except Exception as e:
            raise e
    return userid, client_id

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
