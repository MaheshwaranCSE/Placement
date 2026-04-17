from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    """
    Decorator that checks if the current_user's role is in the specified list.
    Requires @login_required to be used before it.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def faculty_required(f):
    """
    Shorthand decorator for requiring faculty or admin privileges.
    """
    return roles_required('admin', 'faculty')(f)
