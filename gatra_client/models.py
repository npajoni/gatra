from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserLog(models.Model):

    ACCESS_TYPE = (('none', 'none'),
	       ('half_access', 'half_access'),
	       ('full_access', 'full_access'),
	       ('payment', 'payment'))

    customer_id   = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    idp           = models.CharField(max_length=10)
    idp_name      = models.CharField(max_length=255, blank=True)
    country       = models.CharField(max_length=50)
    access        = models.CharField(max_length=30, choices=ACCESS_TYPE)
    device_type   = models.CharField(max_length=100)
    user_agent    = models.CharField(max_length=500)
    source_ip     = models.CharField(max_length=15)
    session_ttl   = models.CharField(max_length=10, blank=True)
    date          = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.customer_name
