import os

class ImproperlyConfigured(Exception):
    """The app is somehow improperly configured"""
    pass

env_msg ="Set the %s environment variable"
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = env_msg % var_name
        raise ImproperlyConfigured(error_msg)
