# -*- coding: utf-8 -*-
import collections
import os
import requests
import yaml


CACHE_SETTINGS = {
    'attribute': 'pyzanata.requests.session',
    'cache_object': None,
}
RESTAPI_SPEC = {}

zanatarestapi = os.path.join(os.path.dirname(__file__), 'restapi.yaml')

with open(zanatarestapi, 'r') as zrapi:
    RESTAPI_SPEC = yaml.load(zrapi)

ZanataCredentials = collections.namedtuple('Connection', 'url user token')


class ZanataMethod(object):

    def __init__(self, endpoint, method, spec):
        self.endpoint = endpoint
        self.method = method
        self.spec = spec

    @property
    def _credentials(self):
        return self.endpoint.resource.client.credentials

    def _path(self, **kwargs):
        return self.spec['endpoint'].format(**kwargs)

    def _url(self, **kwargs):
        return self._credentials.url + self._path(**kwargs)

    @property
    def _headers(self):
        return {'Accept': self.spec['methods'][self.method]}

    @property
    def _session(self):
        """a requests session by zanata user
        """
        # needs evaluation if this can be handled more elegant
        if CACHE_SETTINGS['cache_object'] is not None:
            cache_object = CACHE_SETTINGS['cache_object']
            session_cache = getattr(
                cache_object,
                CACHE_SETTINGS['attribute'],
                None
            )
            if session_cache is None:
                session_cache = dict()
                setattr(
                    cache_object,
                    CACHE_SETTINGS['attribute'],
                    session_cache
                )
        else:
            session_cache = dict()
        session = session_cache.get(self._credentials, None)
        if session is None:
            session = requests.Session()
            session.headers.update({
                'X-Auth-User': self._credentials.user,
                'X-Auth-Token': self._credentials.token,
            })
            session_cache[self._credentials] = session
        return session

    def __call__(self, params=None, data=None, **kwargs):
        req_method = getattr(self._session, self.method.lower())
        resp = req_method(
            self._url(**kwargs),
            data=data,
            params=params,
            headers=self._headers
        )
        return resp


class ZanataEndpoint(object):

    def __init__(self, resource, name, spec):
        self.resource = resource
        self.name = name
        self.spec = spec

    def __getattr__(self, attribute):
        if attribute in self.spec['methods']:
            return ZanataMethod(
                self,
                attribute,
                self.spec
            )
        raise AttributeError(
            'Attribute {0} is not a valid method (nor a usal attribute).\n'
            'valid are:\n'.format(
                attribute,
                '\n'.join(self.spec['methods'].keys())
            )
        )


class ZanataResource(object):

    def __init__(self, client, name, spec):
        self.client = client
        self.name = name
        self.spec = spec

    def __getattr__(self, attribute):
        if attribute in self.spec:
            return ZanataEndpoint(self, attribute, self.spec[attribute])
        raise AttributeError(
            'Attribute {0} is not a valid endpoint (nor a usal attribute).\n'
            'valid are:\n'.format(
                attribute,
                '\n'.join(self.spec.keys())
            )
        )


class ZanataClient(object):

    def __init__(self, credentials):
        """
        credentials - a ZanataCredentials named tuple
        """
        self.credentials = credentials

    def __getattr__(self, attribute):
        if attribute in RESTAPI_SPEC:
            return ZanataResource(self, attribute, RESTAPI_SPEC[attribute])
        raise AttributeError(
            'Attribute {0} is not a valid Resource (nor a usal attribute).'
        )
