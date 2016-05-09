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
        return HttpResponse('', status=http_BAD_REQUEST)


    if 'host' in data.keys() and 'hash' in data.keys() and 'ttl' in data.keys():
        _hash = Hash()
        _hash.valid_host = data['host']
        _hash.valid_hash = data['hash']
        _hash.expiration = datetime.now() + timedelta(0,data['ttl'])
        _hash.save()
        return HttpResponse(data['hash'], status=http_POST_OK)

    return HttpResponse('', status=http_BAD_REQUEST)




def gatraPlayer_PostPlay(request):

    allowed_methods = ['post', 'options']

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join([allowed_methods])
        return response

    if request.method != 'POST':
        return HttpResponse(request.META, status=http_NOT_ALLOWED)

    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('', status=http_BAD_REQUEST)

    if 	'HTTP_GATRA_HASH' in request.META.keys():
        _hash = request.META['HTTP_GATRA_HASH']
        try:
            h = Hash.objects.get(valid_hash = _hash)
        except:
            return HttpResponse(_hash, status=http_UNAUTHORIZED)
    else:
        return HttpResponse('', status=http_UNAUTHORIZED)


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

    if 'season' in jsonData.keys():
        serieSeason = jsonData['season']
    else:
        serieSeason = None

    if 'episode' in jsonData.keys():
        serieEpisode = jsonData['episode']
    else:
        serieEpisode = None

    if 'idp_name' in jsonData.keys():
        idpName = jsonData['idp_name']
    else:
        idpName = ''



        play = Play()
        play.title          = jsonData['title']
        play.season         = serieSeason
        play.episode        = serieEpisode
        play.duration       = jsonData['duration']
        play.device_type    = jsonData['device_type']
        play.user_agent     = get_user_agent(request)
        play.ip_source      = get_client_ip(request)
        play.user_name      = jsonData['user_name']
        play.user_id        = jsonData['user_id']
        play.country        = jsonData['country']
        play.idp            = jsonData['idp']
        play.idp_name       = idpName
        play.media_id       = jsonData['media_id']
        play.media_filename = jsonData['media_filename']
        play.media_type     = jsonData['media_type']

        play.save()

        location = "http://gatra.zolechamendia.net/play/" + str(play.id)
        status = http_POST_OK
        data = {'location' : location};
        response =  HttpResponse(json.dumps(data), status=status, content_type='application/json')
        response['Location'] = location
        return response

    return HttpResponse('', status=http_BAD_REQUEST)


def gatraPlayer_PostEvent(request):

    if request.method != 'POST':
        return HttpResponse('', status=http_NOT_ALLOWED)

    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('', status=http_BAD_REQUEST)

    if ('type' in jsonData.keys() and
    'trigger' in jsonData.keys() and
    'bitrate' in jsonData.keys() and
    'bandwidth' in jsonData.keys() and
    'media_seq' in jsonData.keys() and
    'width' in jsonData.keys() and
    'load_time' in jsonData.keys() and
    'container_height' in jsonData.keys() and
    'container_width' in jsonData.keys() and
    'state' in jsonData.keys() and
    'position' in jsonData.keys() and
    'fullscreen' in jsonData.keys() and
    'quality_label' in jsonData.keys() and
    'volume' in jsonData.keys()):

        try:
            playId = Play.objects.get(id=jsonData['event']['play_id'])
        except ObjectDoesNotExist:
            status = http_NOT_FOUND
            return HttpResponse(json.dumps({'message': 'play_id not found'}), status=status, content_type='application/json')


        event = Event()
        event.play_id           = playId
        event.type              = jsonData['type']
        event.trigger           = jsonData['trigger']
        event.bitrate           = jsonData['bitrate']
        event.bandwidth         = jsonData['bandwidth']
        event.media_seq         = jsonData['media_seq']
        event.width             = jsonData['width']
        event.load_time         = jsonData['load_time']
        event.container_heigth  = jsonData['container_height']
        event.container_weigth  = jsonData['container_width']
        event.state             = jsonDate['state']
        event.position          = jsonDate['position']
        event.fullscreen        = jsonDate['fullscreen']
        event.quality_label     = jsonDate['quality_label']
        event.volume            = jsonDate['volume']

        event.save()

        status = http_POST_OK
        return HttpResponse('', status=status, content_type='application/json')

    return HttpResponse('', status=http_BAD_REQUEST)
