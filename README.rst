Djanginxed
==========
**Django Nginx Memcached integration.**

Provides a view decorator caching content in Memcached for easy retrieval via Nginx. The cache is keyed by md5 of full request path (which includes GET parameters).

.. contents:: Contents
    :depth: 3

Installation
------------

#. Install or add djanginxed to your Python path.
#. Setup Memcached appropriately as described in `Django's cache framework docs <http://docs.djangoproject.com/en/dev/topics/cache/#memcached>`_.
#. Optionally, set the ``CACHE_MIDDLEWARE_KEY_PREFIX`` setting in your Django's settings file -- If the cache is shared across multiple sites using the same Django installation, set this to the name of the site, or some other string that is unique to the Django instance, to prevent key collisions::

    CACHE_MIDDLEWARE_KEY_PREFIX = "site1"

#. Install Nginx with the `set_hash module <https://github.com/simpl/ngx_http_set_hash>`_. This module is required to compute md5 cache keys from within Nginx, i.e.::

    set_md5 $memcached_key $request_uri;
    
#. Configure Nginx for direct Memcached page retrieval, i.e::
    
    location / {
        default_type       text/html;
        set_md5 $memcached_key $request_uri;
        memcached_pass     127.0.0.1:11211;
        error_page         404 405 500 @django;
    }
    
    location @django {
        fastcgi_pass    127.0.0.1:7000;
        fastcgi_param   GATEWAY_INTERFACE   CGI/1.1;
        fastcgi_param   DOCUMENT_URI        $document_uri;
        fastcgi_param   DOCUMENT_ROOT       $document_root;
        fastcgi_param   REQUEST_METHOD      $request_method;
        fastcgi_param   REQUEST_URI         $request_uri;
        fastcgi_param   REMOTE_ADDR         $remote_addr;
        fastcgi_param   REMOTE_PORT         $remote_port;
        fastcgi_param   QUERY_STRING        $query_string;
        fastcgi_param   CONTENT_TYPE        $content_type;
        fastcgi_param   CONTENT_LENGTH      $content_length;
        fastcgi_param   SERVER_ADDR         $server_addr;
        fastcgi_param   SERVER_PROTOCOL     $server_protocol;
        fastcgi_param   SERVER_PORT         $server_port;
        fastcgi_param   SERVER_NAME         $server_name;
        fastcgi_param   SERVER_SOFTWARE     nginx/$nginx_version;
        fastcgi_param   PATH_INFO           $fastcgi_script_name;
    }

#. Optionally, when using a cache key prefix, include it during Nginx ``$memcached_key`` generation::

    set_md5 $memcached_key site1$request_uri;

Usage
-----

Decorators
~~~~~~~~~~

djanginxed.decorators.cache.cache_page
++++++++++++++++++++++++++++++++++++++

The ``cache_page`` decorator caches view response content in Memcached suitable for lookup by Nginx. ``cache_page`` takes a single argument: the cache timeout, in seconds.

Example::

    from djanginxed.decorators.cache import cache_page

    @cache_page(60 * 15)
    def my_view(request):
        ...

This will cache the view's response string in Memcached for 15 minutes (60 * 15), with the cache key generated from the full request path.

**NOTE: The resulting HttpResponse object's content value is stored in Memcached and not the actual HttpResponse object.**

``cache_page`` can also take an optional keyword argument, ``key_prefix``, which works in the same way as the ``CACHE_MIDDLEWARE_KEY_PREFIX`` setting for the middleware. It can be used like this::
    
    @cache_page(60 * 15, key_prefix="site1")
    def my_view(request):
        ...


