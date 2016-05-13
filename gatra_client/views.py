from django.http import HttpResponse


import json

from models import UserLog

http_POST_OK    = 201
http_REQUEST_OK = 200
http_NOT_FOUND  = 404
http_BAD_REQUEST = 400
http_NOT_ALLOWED = 405
http_UNAUTHORIZED = 401

def gatraClient_PostLogin(request):

    allowed_methods = ['POST', 'OPTIONS']

    if request.method == 'OPTIONS':
        response = HttpResponse('', status=http_REQUEST_OK)
        response['Allow'] = ', '.join(allowed_methods)
        return response

    if request.method != 'POST':
        return HttpResponse(request.META, status=http_NOT_ALLOWED)



    try:
        jsonData = json.loads(request.body)
    except:
        return HttpResponse('Could not load json', status=http_BAD_REQUEST)


    if ('customer_id' in jsonData.keys() and
       'customer_name' in jsonData.keys() and
       'idp' in jsonData.keys() and
       'country' in jsonData.keys() and
       'access' in jsonData.keys() and
       'device_type' in jsonData.keys() and
       'user_agent' in jsonData.keys() and
       'source_ip' in jsonData.keys()):

        login = UserLog()

        login.customer_id = jsonData('customer_id')
        login.customer_name = jsonData('customer_name')
        login.idp = jsonData('idp')
        login.idp_name = jsonData('idp_name')
        login.country = jsonData('country')
        login.access = jsonData('access')
        login.device_type = jsonData('device_type')
        login.user_agent = jsonData('user_agent')
        login.source_ip = jsonData('source_ip')

        status = http_POST_OK
        data = {}
        response =  HttpResponse(json.dumps(data), status=status, content_type='application/json')

        return response
    return HttpResponse('Mandatory json value not found', status=http_BAD_REQUEST)