from pyramid.httpexceptions import HTTPBadRequest


def check_csrf_token(request):
    token = request.session.get_csrf_token()
    if token != request.params['csrf_token']:
        raise HTTPBadRequest('CSRF token did not match')


def generate_random_code():
    """Generate random code
    
    """
    import os
    import random
    import hashlib
    import datetime
    key = '%s%s%s' % (
        random.random(), datetime.datetime.now(), os.urandom(60))
    return hashlib.sha1(key).hexdigest()
