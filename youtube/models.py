from django.db import models

# Create your models here.

class YoutubeMetadata(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	publishTimestamp = models.DateTimeField('Date published')
	thumbnailUrl = models.CharField(max_length=200)