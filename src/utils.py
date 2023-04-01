import json
import os
from typing import Generator
from functools import wraps
from flask import Response, redirect, request


def auth_decorator():
    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            # before the function
            pre_shared_key = request.headers.get('Authorization')
            if not pre_shared_key:
                return response_bad_request('Error: Missing Authorization in header.')
            pre_shared_key = pre_shared_key.split(' ')[1]
            if pre_shared_key != os.getenv('PRE_SHARED_KEY'):
                # If the pre_shared_key is not correct, we return 403
                return response_forbidden

            result = f(*args, **kwargs)
            # after the function
            return result
        return __decorator
    return _decorator


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
                        mimetype='text/event-stream',
                        headers={'Access-Control-Allow-Origin': '*'})
    if isinstance(s, str):
        return Response(status=200, response=json.dumps({'msg': s}), content_type='application/json')
    if isinstance(s, dict):
        return Response(status=200, response=json.dumps(s), content_type='application/json')


def response_redirect(url):
    return redirect(url, code=302)
