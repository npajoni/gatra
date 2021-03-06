from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Play (models.Model):

    ACCESS_TYPE = (('none', 'none'),
                   ('half_access', 'half_access'),
                   ('full_access', 'full_access'),
                   ('payment', 'payment'))

    date            = models.DateTimeField(auto_now_add=True)
    title           = models.CharField(max_length=255, blank=True, null=True)
    season          = models.IntegerField(blank=True, null=True)
    episode         = models.IntegerField(blank=True, null=True)
    duration        = models.FloatField(blank=True, null=True)
    device_type     = models.CharField(max_length=40)
    user_agent      = models.CharField(max_length=500)
    ip_source       = models.CharField(max_length=15, blank=True, null=True)
    user_name       = models.CharField(max_length=200, blank=True, null=True)
    user_id         = models.CharField(max_length=50)
    access          = models.CharField(max_length=30, choices=ACCESS_TYPE)
    country         = models.CharField(max_length=20)
    idp             = models.CharField(max_length=50)
    idp_name        = models.CharField(max_length=200, blank=True, null=True)
    media_id        = models.CharField(max_length=10)
    media_filename  = models.CharField(max_length=200, blank=True, null=True)
    media_type      = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.user_name

