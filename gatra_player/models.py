from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Hash(models.Model):
    valid_hash = models.CharField(max_length=32, unique=True)
    valid_host = models.CharField(max_length=15)
    expiration = models.DateTimeField()

    def __unicode__(self):
	    return self.valid_hash

class Event(models.Model):
    play_id 		    = models.ForeignKey('Play')
    date  		        = models.DateTimeField(auto_now_add=True)
    type		        = models.CharField(max_length=50)
    trigger		        = models.CharField(max_length=20)
    bitrate		        = models.IntegerField()
    bandwidth		    = models.IntegerField()
    media_seq		    = models.IntegerField()
    width		        = models.IntegerField()
    load_time		    = models.FloatField()
    container_height	= models.IntegerField()
    container_width	    = models.IntegerField()
    state		        = models.CharField(max_length=20)
    position		    = models.FloatField()
    fullscreen		    = models.BooleanField()
    quality_label	    = models.CharField(max_length=20)
    volume		        = models.IntegerField()

    def __unicode__(self):
	    return self.type


class Play (models.Model):
    date		    = models.DateTimeField(auto_now_add=True)
    title		    = models.CharField(max_length=255)
    season		    = models.IntegerField(blank=True, null=True)
    episode		    = models.IntegerField(blank=True, null=True)
    duration		= models.FloatField()
    device_type    	= models.CharField(max_length=40)
    user_agent     	= models.CharField(max_length=500)
    ip_source		= models.CharField(max_length=15)
    user_name	   	= models.CharField(max_length=200)
    user_id		    = models.CharField(max_length=50)
    country		    = models.CharField(max_length=20)
    idp		    	= models.CharField(max_length=50)
    idp_name		= models.CharField(max_length=200, blank=True)
    media_id	   	= models.CharField(max_length=10)
    media_filename 	= models.CharField(max_length=200)
    media_type	   	= models.CharField(max_length=10)
    
    def __unicode__(self):
	    return self.user_name

