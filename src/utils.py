import json
from typing import Generator

from flask import Response, redirect

response_ok = Response(status=200, response=json.dumps({'msg': 'OK!'}), content_type='application/json')
response_error = Response(status=500, response=json.dumps({'msg': 'Something wrong!'}), content_type='application/json')
response_not_found = Response(status=404, response=json.dumps({'msg': 'Not Found!'}), content_type='application/json')
response_forbidden = Response(status=403, response=json.dumps({'msg': 'Invalid token!'}), content_type='application/json')
response_not_verified = Response(status=401, response=json.dumps({'msg': 'Email not verified!'}), content_type='application/json')
response_not_enough_token = Response(status=402, response=json.dumps({'msg': 'Insufficient token (client)!'}), content_type='application/json')
response_not_enough_token_user = Response(status=402, response=json.dumps({'msg': 'Insufficient token (user)!'}), content_type='application/json')

def response_bad_request(s):
    if isinstance(s, str):
        return Response(status=400, response=json.dumps({'msg': s}), content_type='application/json')
    if isinstance(s, dict):
        return Response(status=400, response=json.dumps(s), content_type='application/json')


def response_ratelimit(s):
    if isinstance(s, str):
        return Response(status=429, response=json.dumps({'msg': s}), content_type='application/json')
    if isinstance(s, dict):
        return Response(status=429, response=json.dumps(s), content_type='application/json')


def response_normal(s):
    if isinstance(s, Generator):
        return Response(status=200, response=s,
                        mimetype='text/data-stream',
                        headers={'Access-Control-Allow-Origin': '*'})
    if isinstance(s, str):
        return Response(status=200, response=json.dumps({'msg': s}), content_type='application/json')
    if isinstance(s, dict):
        return Response(status=200, response=json.dumps(s), content_type='application/json')


def response_redirect(url):
    return redirect(url, code=302)
