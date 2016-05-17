from django.http import HttpResponse
from datetime import datetime
from datetime import timedelta

import json



# Create your views here.
from models import Hash
from models import Event
from models import Play

from django.core.exceptions import *

http_POST_OK    = 201
http_REQUEST_OK = 200
http_NOT_FOUND  = 404
http_BAD_REQUEST = 400
http_NOT_ALLOWED = 405
http_UNAUTHORIZED = 401


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')


def gatraPlayer_PostHash(request):
    if request.method != 'POST':
        return HttpResponse('', status=http_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except:
        return HttpResponse('Could not load json', status=http_BAD_REQUEST)

    if 'host' in data.keys() and 'hash' in data.keys() and 'ttl' in data.keys():
        _hash = Hash()
        _hash.valid_host = data['host']
        _hash.valid_hash = data['hash']
        _hash.expiration = datetime.now() + timedelta(0,data['ttl'])
        _hash.save()
        return HttpResponse(data['hash'], status=http_POST_OK)

    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)


def gatraPlayer_PostPlay(request):

    allowed_methods = ['POST', 'OPTIONS']

    if request.method == 'OPTIONS':
        response = HttpResponse('', status=http_REQUEST_OK)
        response['Allow'] = ', '.join(allowed_methods)
        return response

    if request.method != 'POST':
        return HttpResponse(request.META, status=http_NOT_ALLOWED)

    if 'HTTP_GATRA_HASH' in request.META.keys():
        _hash = request.META['HTTP_GATRA_HASH']
        try:
            h = Hash.objects.get(valid_hash = _hash)
        except:
            return HttpResponse(_hash, status=http_UNAUTHORIZED)
    else:
        return HttpResponse('', status=http_UNAUTHORIZED)

    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('Could not load json', status=http_BAD_REQUEST)

    if ('title' in jsonData.keys() and
       'duration' in jsonData.keys() and
       'device_type' in jsonData.keys() and
       'user_name' in jsonData.keys() and
       'user_id' in jsonData.keys() and
       'country' in jsonData.keys() and
       'idp' in jsonData.keys() and
       'media_id' in jsonData.keys() and
       'media_filename' in jsonData.keys() and
       'media_type' in jsonData.keys()):

        play = Play()
        play.title          = jsonData['title']
        play.duration       = jsonData['duration']
        play.device_type    = jsonData['device_type']
        play.user_agent     = get_user_agent(request)
        play.ip_source      = get_client_ip(request)
        play.user_name      = jsonData['user_name']
        play.user_id        = jsonData['user_id']
        play.country        = jsonData['country']
        play.idp            = jsonData['idp']
        play.media_id       = jsonData['media_id']
        play.media_filename = jsonData['media_filename']
        play.media_type     = jsonData['media_type']

	if 'season' in jsonData.keys():
	    play.season = jsonData['season']

	if 'episode' in jsonData.keys():
	    play.episode = jsonData['episode']

	if 'idp_name' in jsonData.keys():
	    play.idp_name = jsonData['idp_name']

        play.save()

        location = "http://gatra.zolechamedia.net/play/" + str(play.id) + "/"
        status = http_POST_OK
        data = {'location' : location};
        response =  HttpResponse(json.dumps(data), status=status, content_type='application/json')
    #    response['Location'] = location
        return response

    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)


def gatraPlayer_PostEvent(request, id):

    allowed_methods = ['POST', 'OPTIONS']

    if request.method == 'OPTIONS':
        response = HttpResponse('', status=http_REQUEST_OK)
        response['Allow'] = ', '.join(allowed_methods)
        return response

    if request.method != 'POST':
        return HttpResponse('', status=http_NOT_ALLOWED)

    if 'HTTP_GATRA_HASH' in request.META.keys():
        _hash = request.META['HTTP_GATRA_HASH']
        try:
            h = Hash.objects.get(valid_hash = _hash)
        except:
            return HttpResponse(_hash, status=http_UNAUTHORIZED)
    else:
        return HttpResponse('', status=http_UNAUTHORIZED)

    if id is None:
	return HttpResponse('', status=http_BAD_REQUEST)

    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('Could not load json', status=http_BAD_REQUEST)

    if ('type' in jsonData.keys() and
    'trigger' in jsonData.keys() and
    'width' in jsonData.keys() and
    'container_height' in jsonData.keys() and
    'container_width' in jsonData.keys() and
    'state' in jsonData.keys() and
    'position' in jsonData.keys() and
    'fullscreen' in jsonData.keys() and
    'volume' in jsonData.keys()):

	try:
	    play_id = Play.objects.get(id = id)
	except:
	    return HttpResponse('Play ID not found', status=http_BAD_REQUEST)

	event = Event()
        event.play		= play_id
        event.type              = jsonData['type']
        event.trigger           = jsonData['trigger']
        event.width             = jsonData['width']
        event.container_height  = jsonData['container_height']
        event.container_width	= jsonData['container_width']
        event.state             = jsonData['state']
        event.position          = jsonData['position']
        event.fullscreen        = jsonData['fullscreen']
        event.volume            = jsonData['volume']

        if 'bitrate' in jsonData.keys():
	    event.bitrate = jsonData['bitrate']

	if 'bandwidth' in jsonData.keys():
	    event.bandwidth = jsonData['bandwidth']

	if 'media_seq' in jsonData.keys():
	    event.media_seq = jsonData['media_seq']

	if 'load_time' in jsonData.keys():
	    event.load_time = jsonData['load_time']

	if 'quality_label' in jsonData.keys():
	    event.quality_label     = jsonData['quality_label']

        event.save()

        status = http_POST_OK
        return HttpResponse('', status=status, content_type='application/json')

    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)
