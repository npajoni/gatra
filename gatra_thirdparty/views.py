from django.http import HttpResponse
from user_agents import parse

import json

# Create your views here.
from models import Play

http_POST_OK = 201
http_NOT_FOUND = 404
http_BAD_REQUEST = 400
http_NOT_ALLOWED = 405


def gatraThirdparty_PostPlay(request):
    allowed_methods = ['POST', 'OPTIONS']

    if request.method == 'OPTIONS':
        response = HttpResponse('', status=http_REQUEST_OK)
        response['Allow'] = ', '.join(allowed_methods)
        return response

    if request.method != 'POST':
        return HttpResponse('', status=http_NOT_ALLOWED)

    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('Could not load json', status=http_BAD_REQUEST)

    if ('device_type' in jsonData.keys() and
        'user_agent' in jsonData.keys() and
        'user_id' in jsonData.keys() and
        'access' in jsonData.keys() and
        'country' in jsonData.keys() and
        'idp' in jsonData.keys() and
        'media_id' in jsonData.keys()):

        play = Play()
        if 'title' in jsonData.keys():
            play.title = jsonData['title']
        if 'duration' in jsonData.keys():
            play.duration = jsonData['duration']
        play.device_type = jsonData['device_type']
        play.user_agent = jsonData['user_agent']
        if 'ip_source' in jsonData.keys():
            play.ip_source = jsonData['ip_source']
        if 'user_name' in jsonData.keys():
            play.user_name = jsonData['user_name']
        play.user_id = jsonData['user_id']
        play.access = jsonData['access']
        play.country = jsonData['country']
        play.idp = jsonData['idp']
        play.media_id = jsonData['media_id']
        if 'media_filename' in jsonData.keys():
            play.media_filename = jsonData['media_filename']
        if 'media_type' in jsonData.keys():
            play.media_type = jsonData['media_type']

        if 'season' in jsonData.keys():
            play.season = jsonData['season']

        if 'episode' in jsonData.keys():
            play.episode = jsonData['episode']

        if 'idp_name' in jsonData.keys():
            play.idp_name = jsonData['idp_name']

        play.save()

        status = http_POST_OK
        response = HttpResponse('', status=status, content_type='application/json')
        return response

    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)