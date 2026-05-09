import config
from sanic_ext import openapi as _openapi

class _NoOpOpenAPI:
    @staticmethod
    def summary(text):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def description(text):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def tag(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def parameter(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def response(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def body(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    @staticmethod
    def deprecated(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

openapi = _openapi if config.SANIC_DOC_API else _NoOpOpenAPI()