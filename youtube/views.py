from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import YoutubeMetadata
import json
import requests
import dateutil.parser
from django.core.paginator import Paginator

def index(request):

    t=1
    data = fetchVideos(t)
    while('items' not in data):
        t=t+1
        data = fetchVideos(t)
        if(data==None):
            return HttpResponse("None of the supplied API Keys work.")

    response = []
    
    for i in data['items']:
        entry = {}
        entry['title'] = i['snippet']['title']
        entry['description'] = i['snippet']['description']
        entry['publishedTimestamp'] = str(i['snippet']['publishedAt'])
        entry['thumbnailUrl'] = i['snippet']['thumbnails']['default']['url']
        response.append(entry)

        dbRow = YoutubeMetadata()
        dbRow.videoId = i['id']['videoId']
        dbRow.title = entry['title']
        dbRow.description = entry['description']
        dbRow.publishTimestamp = str(dateutil.parser.parse(entry['publishedTimestamp']))
        dbRow.thumbnailUrl = entry['thumbnailUrl']
        dbRow.save()
    
    res = json.dumps(response)
    paginator = Paginator(response,10)
    page = request.GET.get('page')
    finalResponse = paginator.get_page(page)
    template = loader.get_template('youtube/index.html')
    return HttpResponse(template.render({'data': finalResponse}, request))

def fetchVideos(t):

    json_data = open('./keys.json')
    secret_keys = json.load(json_data)

    if('key' + str(t) in secret_keys['YOUTUBE_DATA_API_KEYS']):
        api_key = secret_keys['YOUTUBE_DATA_API_KEYS']['key' + str(t)]
    else:
        return None

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
    return data