from django.db import models

# Create your models here.

class YoutubeMetadata(models.Model):
	videoId = models.CharField(max_length=200, primary_key=True)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	publishTimestamp = models.DateTimeField('Date published')
	thumbnailUrl = models.CharField(max_length=200)