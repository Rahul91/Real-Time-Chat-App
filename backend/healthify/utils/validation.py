from functools import wraps
import re

# Ref http://emailregex.com/
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

__author__ = 'rahul'


# IMPORTANT Do not make db operations here

def not_empty(param, err_code, req=False, var_type=basestring, default_val=None):
    def wrapper(fn):
        # A side effect of using decorators is that the function that gets wrapped loses it's
        # natural __name__, __doc__, and __module__ attributes.
        # wraps decorator takes a function used in a decorator and adds the functionality of
        # copying over the function name, docstring, arguments list, etc.
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                # val = kwargs[param] if req else kwargs.get(param)
                if req:
                    val = kwargs[param]
                else:
                    val = kwargs.get(param) if kwargs.get(param) is not None else default_val
                    kwargs.update({param: val})
            except KeyError:
                raise KeyError(err_code)
            if type(val) == bool and var_type == bool:
                return fn(*args, **kwargs)
            elif (var_type == int) and isinstance(val, var_type) and (val or val == 0):
                return fn(*args, **kwargs)
            elif (var_type == float) and isinstance(val, (int, float)) and (val or val == 0):
                return fn(*args, **kwargs)
            elif isinstance(val, var_type) and val:
                return fn(*args, **kwargs)
            elif (val is None) and (not req):
                return fn(*args, **kwargs)
            raise ValueError(err_code)
        return decorator

    return wrapper


def allowed_entities(param, param_list, err_code):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if kwargs.get(param) in param_list:
                return fn(*args, **kwargs)
            raise ValueError(err_code + '-' + kwargs.get(param).upper())
        return decorator
    return wrapper


def any_of(params, err_code):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            vals = [kwargs.get(param) for param in params]
            if any(vals):
                return fn(*args, **kwargs)
            raise ValueError(err_code)
        return decorator
    return wrapper


def valid_username(param, err_code):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            email = kwargs.get(param)
            if email and isinstance(email, basestring) and EMAIL_REGEX.match(email):
                return fn(*args, **kwargs)
            raise ValueError(err_code)

        return decorator

    return wrapper


def non_empty_str(val):
    if isinstance(val, basestring) and val.strip():
        return val
    raise ValueError
