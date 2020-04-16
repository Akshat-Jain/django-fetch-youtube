from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import YoutubeMetadata
import json
import requests
import dateutil.parser

# Create your views here.
def index(request):

    data = fetchVideos()

    # data = YoutubeMetadata.objects.all()
    response = []
    
    for i in data['items']:
        entry = {}
        # entry['avds'] = str(i.publishTimestamp)
        entry['title'] = i['snippet']['title']
        entry['description'] = i['snippet']['description']
        entry['publishedTimestamp'] = str(i['snippet']['publishedAt'])
        entry['thumbnailUrl'] = i['snippet']['thumbnails']['default']['url']
        response.append(entry)

        dbRow = YoutubeMetadata()
        dbRow.title = entry['title']
        dbRow.description = entry['description']
        dbRow.publishTimestamp = str(dateutil.parser.parse(entry['publishedTimestamp']))
        dbRow.thumbnailUrl = entry['thumbnailUrl']
        dbRow.save()
        # print('dbrow.dbRow.publishedTimestamp ' + str(dbRow.publishTimestamp))
        # print('entry[publishedTimestamp] = ' + entry['publishedTimestamp'])
        # print('dateutil Timestamp = ' + str(dateutil.parser.parse(entry['publishedTimestamp'])))
    
    res = json.dumps(response)
    return HttpResponse(res)

def fetchVideos():
    queryArguments = {
    'order':'date',
    'part':'snippet',
    'maxResults': 5,
    'publishedAfter':'2000-04-04T15:51:12.000Z',
    'q':'cricket',
    'type':'video',
    'key':'AIzaSyAitzsrJ99oB7zwAHqdPb60RhAqwSVDGro'
    }
    url = 'https://content.googleapis.com/youtube/v3/search'
    r = requests.get(url,params=queryArguments)
    data = r.json()
    return data
# def backgroundTask(response):
#   return json.dumps(response)