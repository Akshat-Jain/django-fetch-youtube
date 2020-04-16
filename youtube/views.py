from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import YoutubeMetadata
import json

# Create your views here.
def index(request):
    data = YoutubeMetadata.objects.all()
    response = []
    
    for i in data:
    	entry = {}
    	entry['title'] = i.title
    	entry['description'] = i.description
    	entry['publishTimestamp'] = str(i.publishTimestamp)
    	entry['thumbnailUrl'] = i.thumbnailUrl
    	response.append(entry)
    
    res = json.dumps(response)
    return HttpResponse(res)