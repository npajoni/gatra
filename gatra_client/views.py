from django.http import HttpResponse

#
# https://github.com/selwin/python-user-agents
#

from user_agents import parse

import json

from models import UserLog

http_POST_OK      = 201
http_REQUEST_OK   = 200
http_NOT_FOUND    = 404
http_BAD_REQUEST  = 400
http_NOT_ALLOWED  = 405
http_UNAUTHORIZED = 401

def gatraClient_PostLogin(request):

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


    if ('customer_id'   in jsonData.keys() and
        'customer_name' in jsonData.keys() and
        'idp'           in jsonData.keys() and
        'country'       in jsonData.keys() and
        'access'        in jsonData.keys() and
        'user_agent'    in jsonData.keys() and
        'source_ip'     in jsonData.keys()):

        login = UserLog()

        login.customer_id   = jsonData['customer_id']
        login.customer_name = jsonData['customer_name']
        login.idp           = jsonData['idp']
	if 'idp_name' in jsonData.keys():
    	    login.idp_name      = jsonData['idp_name']
	if 'session_ttl' in jsonData.keys():
	    login.session_ttl   = jsonData['session_ttl']
        login.country       = jsonData['country']
        login.access        = jsonData['access']
        login.user_agent    = jsonData['user_agent']
        login.source_ip     = jsonData['source_ip']

	ua = parse(login.user_agent)
	if ua.is_mobile:
	    login.device_type = 'mobile'
	elif ua.is_tablet:
	    login.device_type = 'tablet'
	elif ua.is_pc:
	    login.device_type = 'desktop'
	else:
	    login.device_type = 'unknown'

	login.save()

        status = http_POST_OK
        data = {}
        response =  HttpResponse(json.dumps(data), status=status, content_type='application/json')
        return response

    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)
