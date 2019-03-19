"""
Copyright 2019 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
   disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
   disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products 
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open Source Initiative: 
http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""
from typing import Callable, Optional, Type

import requests

from base import RequestParamsType, ResponseType

__author__ = "EUROCONTROL (SWIM)"


class RequestHandler:
    """
        Wraps up the basic expected request methods of a REST client such as get, post, delete, put.
        The default used handler is: requests.session
    """
    _URL_BASE_FORMAT = "{scheme}://{host}/"

    def __init__(self,
                 host: str,
                 https: bool = True,
                 timeout: int = 30,
                 auth: Optional[tuple] = None,
                 request_handler_maker: Optional[Callable] = None) -> None:
        """
        :param host: The host of the service to be accessed via the client
        :param https: indicates whether the host serves over TSL or not
        :param auth: pair of username and password
        :param timeout: How many seconds to wait for the server to send data before giving up
        :param request_handler_maker: a callback which instantiates a custom request handler
        """

        self.timeout = timeout
        self.auth = auth or ()
        self._request_handler = request_handler_maker() if request_handler_maker else requests.session()
        self._base_url = RequestHandler._URL_BASE_FORMAT.format(host=host, scheme='https' if https else 'http')

    def get(self,
            url: str,
            params: Optional[RequestParamsType] = None,
            **kwargs: str) -> Type[ResponseType]:
        """
        Implements a GET request

        :param url: the full URL of the Request
        :param params: dict, list of tuples or bytes to send in the query string for the Request
        :param kwargs: optional arguments
        :return: Python object wrapping up Response data after a Request, i.e. requests.Response
        """
        return self._do_request(self._request_handler.get, url=url, params=params, **kwargs)

    def delete(self,
               url: str,
               params: Optional[RequestParamsType] = None,
               **kwargs: str) -> Type[ResponseType]:
        """
        Implements a DELETE request

        :param url: the full URL of the request
        :param params: dict, list of tuples or bytes to send in the query string for the Request
        :param kwargs: optional extra parameters
        :return: Python object wrapping up Response data after a Request, i.e. requests.Response
        """
        return self._do_request(self._request_handler.delete, url=url, params=params, **kwargs)

    def post(self,
             url: str,
             data: Optional[RequestParamsType] = None,
             json: Optional[RequestParamsType] = None,
             **kwargs: str) -> Type[ResponseType]:
        """
        Implements a POST request

        :param url: the full URL of the request
        :param data: dict, list of tuples, bytes, or file-like object to send in the body of the request
        :param json: A JSON serializable Python object to send in the body of the Request
        :param kwargs: optional extra parameters
        :return: Python object wrapping up Response data after a Request, i.e. requests.Response
        """
        return self._do_request(self._request_handler.post, url=url, data=data, json=json, **kwargs)

    def put(self,
            url: str,
            data: Optional[RequestParamsType] = None,
            json: Optional[RequestParamsType] = None,
            **kwargs: str) -> Type[ResponseType]:
        """
        Implements a PUT request

        :param url:
        :param data: dict, list of tuples, bytes, or file-like object to send in the body of the request
        :param json: A JSON serializable Python object to send in the body of the Request
        :param kwargs: optional extra parameters
        :return: Python object wrapping up Response data after a Request, i.e. requests.Response
        """
        return self._do_request(self._request_handler.put, url=url, data=data, json=json, **kwargs)

    def _do_request(self, request_method: Callable, url: str, **kwargs: str) -> Type[ResponseType]:
        """

        :param request_method:
        :param url:
        :param kwargs: optional extra parameters
        :return:
        """
        url: str = self._base_url + url

        return request_method(url, **kwargs)
