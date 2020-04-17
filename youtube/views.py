from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import YoutubeMetadata
import json
import requests
import dateutil.parser
from django.core.paginator import Paginator
import time
from threading import Thread

def index(request):
    # fetchVideos()
    # t=1
    # data = fetchVideos(t)
    # while('items' not in data):
    #     t=t+1
    #     data = fetchVideos(t)
    #     if(data==None):
    #         return HttpResponse("None of the supplied API Keys work.")
    # startFetching()
    response = []
    data = YoutubeMetadata.objects.all()
    for i in data:
        entry = {}
        entry['title'] = i.title
        entry['description'] = i.description
        entry['publishedTimestamp'] = str(i.publishTimestamp)
        entry['thumbnailUrl'] = i.thumbnailUrl
        response.append(entry)

    paginator = Paginator(response,10)
    page = request.GET.get('page')
    finalResponse = paginator.get_page(page)
    template = loader.get_template('youtube/index.html')
    return HttpResponse(template.render({'data': finalResponse}, request))

def fetchVideos():
    # lol=1
    # while(True):
    #     print(lol)
    #     time.sleep(3)
    #     lol = lol + 1
    #     if(lol==5):
    #         break
    json_data = open('./keys.json')
    secret_keys = json.load(json_data)

    while(True):
        t = 1
        data = {}
        while('items' not in data):
            if('key' + str(t) in secret_keys['YOUTUBE_DATA_API_KEYS']):
                api_key = secret_keys['YOUTUBE_DATA_API_KEYS']['key' + str(t)]
            else:
                break
            queryArguments = {
            'order': 'date',
            'part': 'snippet',
            'maxResults': 25, # Values must be within the range: [0, 50] as per YouTube Data API design
            'publishedAfter': '2000-04-04T15:51:12.000Z',
            'q': 'Game of Thrones',
            'type': 'video',
            'key': api_key
            }
            url = 'https://content.googleapis.com/youtube/v3/search'
            r = requests.get(url,params=queryArguments)
            data = r.json()
            t = t+1

        for i in data['items']:
            entry = {}
            dbRow = YoutubeMetadata()
            dbRow.videoId = i['id']['videoId']
            dbRow.title = i['snippet']['title']
            dbRow.description = i['snippet']['description']
            dbRow.publishTimestamp = str(i['snippet']['publishedAt'])
            dbRow.thumbnailUrl = i['snippet']['thumbnails']['default']['url']
            dbRow.save()
        time.sleep(10)

def startFetching(request):
    process = Thread(target=fetchVideos)
    process.start()
    return HttpResponse("A background asynchronorous job to fetch videos has been triggered.")