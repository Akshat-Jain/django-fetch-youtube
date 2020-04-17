from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import YoutubeMetadata
import json
import requests
import dateutil.parser
from django.core.paginator import Paginator

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
    # return HttpResponse(finalResponse)
    template = loader.get_template('youtube/index.html')
    return HttpResponse(template.render({'data': finalResponse}, request))

def fetchVideos():
    queryArguments = {
    'order':'date',
    'part':'snippet',
    'maxResults': 25, # Values must be within the range: [0, 50] as per YouTube Data API design
    'publishedAfter':'2000-04-04T15:51:12.000Z',
    'q':'Game of Thrones',
    'type':'video',
    'key':'AIzaSyAlt-If_97q82M36V6qjYHxaZuX01RmulQ'
    }
    url = 'https://content.googleapis.com/youtube/v3/search'
    r = requests.get(url,params=queryArguments)
    data = r.json()
    return data
