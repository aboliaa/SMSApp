from functools import wraps
from flask import request, abort

from functionality.auth import check_auth

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Flask can decode the Basic Authorization header,
        # into the username and password.
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            abort(401)
        return f(*args, **kwargs)
    return decorated