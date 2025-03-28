import six

from django.http import HttpResponse
from django.urls import re_path

from restea.adapters.base import (
    BaseResourceWrapper,
    BaseRequestWrapper,
)


class DjangoRequestWrapper(BaseRequestWrapper):
    '''
    Object wrapping Django request object.
    '''
    @property
    def method(self):
        '''
        Returns a payload sent to server

        :returns: string -- raw value of payload sent to server
        '''
        return self._original_request.method

    @property
    def headers(self):
        '''
        Returns a headers dict

        :returns: dict -- received request headers
        '''
        return self._original_request.META

    def get(self, value):
        '''
        Returns HTTP method for the current request

        :returns: string -- HTTP method name
        '''
        return self._original_request.GET.get(value)

    @property
    def data(self):
        '''
        Returns a value from the HTTP GET "map"

        :param value: string -- key from GET
        :returns: string -- value from GET or None if anything is found
        '''
        return self._original_request.body


class DjangoResourceRouter(BaseResourceWrapper):
    '''
    Wraps over Django views, implements Django view API and creates routing in
    the Django urlrouter format
    '''
    request_wrapper_class = DjangoRequestWrapper

    def prepare_response(self, content, status_code, content_type, headers):
        response = HttpResponse(
            content,
            content_type=content_type,
            status=status_code
        )
        for name, value in six.iteritems(headers):
            response[name] = value
        return response

    def get_routes(self, path='', iden_format=r'(?P<iden>\w+)'):
        '''
        Prepare routes for the given REST resource

        :param path: string -- base path for the REST resource
        :param iden: string -- format for identifier, for instance might be
        used to make composite identifier
        '''
        return [
            re_path(
                r'^{}(?:\.(?P<data_format>\w+))?$'.format(path),
                self.wrap_request
            ),
            re_path(
                r'^{}/{}(?:\.(?P<data_format>\w+))?$'.format(
                    path, iden_format),
                self.wrap_request
            )
        ]
