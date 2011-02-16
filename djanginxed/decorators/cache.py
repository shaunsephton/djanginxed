from functools import wraps
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import decorator_from_middleware, available_attrs

def get_cache_key(request, key_prefix, key_generator=None):
    """
    The cache is keyed by md5 of full request path including GET parameters, 
    thus enabling Memcached lookup straight from Nginx.

    If key_generator is provided it is used instead to generate a key. 
    key_generator should be a callable accepting a request object and returning a string to be used as cache key.
    
    Additionally there is the key prefix that is used to distinguish different
    cache areas in a multi-site setup. The key prefix is prepended to the request path md5.
    """
    key = key_generator(request) if key_generator else hashlib.md5(request.get_full_path()).hexdigest() 
    key_prefix = key_prefix or settings.CACHE_MIDDLEWARE_KEY_PREFIX
    return key_prefix + key

def cache_page(timeout, key_prefix='', key_generator=None):
    """
    Decorator for views that tries getting the page from the cache and
    populates the cache if the page isn't in the cache yet.
    
    The cache is keyed by md5 of full request path including GET parameters, 
    thus enabling Memcached lookup straight from Nginx.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            cache_key = get_cache_key(request, key_prefix, key_generator)
            response = cache.get(cache_key, None)
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response.content, timeout)
            return response
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator
