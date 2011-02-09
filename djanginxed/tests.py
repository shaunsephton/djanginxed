import hashlib

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.test import TestCase

from djanginxed.decorators import cache
from snippetscream import RequestFactory

class DecoratorCacheTestCase(TestCase):
    def test_get_cache_key(self):
        request = RequestFactory().get('/')

        # With no prefix provided or present in settings, return md5 only.
        key = cache.get_cache_key(request, '')
        self.assertEqual(len(key), 32)
        self.assertEqual(key, hashlib.md5('/').hexdigest())
        
        # With prefix provided through param, return prefix + md5.
        key = cache.get_cache_key(request, 'prefix')
        self.assertEqual(key, 'prefix' + hashlib.md5('/').hexdigest())
        
        # With no prefix provided through param, return settings prefix + md5.
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = 'prefix'
        key = cache.get_cache_key(request, '')
        self.assertEqual(key, 'prefix' + hashlib.md5('/').hexdigest())
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = ''
        
        # Get paramaters should be included when calculating md5.
        request = RequestFactory().get('/?foo=bar')
        key = cache.get_cache_key(request, '')
        self.assertEqual(key, hashlib.md5('/?foo=bar').hexdigest())
    
    def test_cache_page(self):
        def my_view(request):
            return HttpResponse("response")

        # On cache miss return HttpResponse object with "response" content.
        my_view_cached = cache.cache_page(123)(my_view)
        self.assertEqual(my_view_cached(HttpRequest()).content, "response")

        # On cache hit return "response" content.
        my_view_cached = cache.cache_page(123)(my_view)
        self.assertEqual(my_view_cached(HttpRequest()), "response")
