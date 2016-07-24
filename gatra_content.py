import datetime
import django
import os
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gatra.settings")
django.setup()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Base Exceptions
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.core.exceptions import *

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# App Model
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from gatra_player.models import Content

import httplib2
import urlparse
import json
import time


class conectorError(Exception):
    def __init__(self, value, critical=False):
        self.value = value
        self.critical = critical

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.value



class contentConector(object):
    def __init__(self, server = '', api = ''):
        self.baseuri    	= 'http://%s' % (server)
        self.baseapi    	= api
    
    def get(self):
        method  = 'GET'
        body    = ''

        if self.baseapi is not None:
            uri = urlparse.urlparse(self.baseuri + self.baseapi)
        else:
	    raise conectorError('get(): api can not be None')

	print uri
        h = httplib2.Http()
        try:
            response, content = h.request(uri.geturl(), method, body)
        except socket.error as err:
            raise conectorError(err)

        if response['status'] == '200':
            return content
        elif response['status'] == '404':
    	    return None


conn    = contentConector('www.hotgo.tv', '/es/api/1.0/content')
content = json.loads(conn.get())
for c in content:
    try:
	content = Content.objects.get(media_id=c['house id'])
    except:
	print c['house id']
	new = Content()
        new.title    = c['name']
        new.category = c['category'] 
        new.channel  = c['channel']
        new.media_id = c['house id']
        new.cast     = c['Elenco']
        new.save()



