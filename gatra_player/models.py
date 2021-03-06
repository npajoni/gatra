from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Hash(models.Model):
    valid_hash  = models.CharField(max_length=32, unique=True)
    user_name   = models.CharField(max_length=200, blank=True)
    title       = models.CharField(max_length=255, blank=True)
    valid_host  = models.CharField(max_length=15)
    expiration  = models.DateTimeField()

    def __unicode__(self):
        return self.valid_hash


class Event(models.Model):
    play                = models.ForeignKey('Play')
    date                = models.DateTimeField(auto_now_add=True)
    type                = models.CharField(max_length=50)
    trigger             = models.CharField(max_length=20)
    bitrate             = models.IntegerField(blank=True, null=True)
    bandwidth           = models.IntegerField(blank=True, null=True)
    media_seq           = models.IntegerField(blank=True, null=True)
    width               = models.IntegerField()
    load_time           = models.FloatField(blank=True, null=True)
    container_height    = models.IntegerField()
    container_width     = models.IntegerField()
    state               = models.CharField(max_length=20)
    position            = models.FloatField()
    fullscreen          = models.BooleanField()
    quality_label       = models.CharField(max_length=20, blank=True)
    volume              = models.IntegerField()

    def __unicode__(self):
        return self.type


class Play (models.Model):
    date            = models.DateTimeField(auto_now_add=True)
    title           = models.CharField(max_length=255)
    season          = models.IntegerField(blank=True, null=True)
    episode         = models.IntegerField(blank=True, null=True)
    duration        = models.FloatField()
    device_type     = models.CharField(max_length=40)
    user_agent      = models.CharField(max_length=500)
    ip_source       = models.CharField(max_length=15)
    user_name       = models.CharField(max_length=200)
    user_id         = models.CharField(max_length=50)
    country         = models.CharField(max_length=20)
    idp             = models.CharField(max_length=50)
    idp_name        = models.CharField(max_length=200, blank=True)
    media_id        = models.CharField(max_length=10)
    media_filename  = models.CharField(max_length=200)
    media_type      = models.CharField(max_length=10)
    reduced         = models.BooleanField(default=False)
    rep_time        = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.user_name

class Content(models.Model):
    title       = models.CharField(max_length=255)
    media_id    = models.CharField(max_length=10)
    category    = models.CharField(max_length=510)
    channel     = models.CharField(max_length=50)
    cast        = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return self.title