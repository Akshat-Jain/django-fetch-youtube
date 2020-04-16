from django.shortcuts import render
from django.http import HttpResponse
from .models import YoutubeMetadata
# Create your views here.
def index(request):
    x = YoutubeMetadata.objects.all()
    output = ', '.join([q.title for q in x])
    return HttpResponse(output)
    # return HttpResponse("Welcome to AkJn's world! :)")