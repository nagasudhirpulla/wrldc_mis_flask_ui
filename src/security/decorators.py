# https://github.com/maxcountryman/flask-login/issues/421
from flask_login import current_user
import werkzeug
from functools import wraps

def role_required(role: str):
    def _role_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                raise werkzeug.exceptions.Forbidden()
            if not current_user.has_role(role):
                raise werkzeug.exceptions.Unauthorized()
            return f(*args, **kwargs)
        return decorated_view
    return _role_required


def roles_required(roles: list, require_all=False):
    def _roles_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError('Empty list used when requiring a role.')
            if not current_user.is_authenticated:
                raise werkzeug.exceptions.Forbidden()
            if require_all and not all(current_user.has_role(role) for role in roles):
                raise werkzeug.exceptions.Unauthorized()
            elif not require_all and not any(current_user.has_role(role) for role in roles):
                raise werkzeug.exceptions.Unauthorized()
            return f(*args, **kwargs)
        return decorated_view
    return _roles_required
