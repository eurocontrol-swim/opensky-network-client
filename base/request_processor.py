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
import typing as t

from base import BaseModel
from base.typing import RequestParams, RequestHandler
from base.errors import APIError

__author__ = "EUROCONTROL (SWIM)"


class RequestProcessor:
    """Manages the entire flow of a HTTP Request/Response"""

    def __init__(self, request_handler: t.Type[RequestHandler]) -> None:
        """
        :param request_handler: an instance of an object capable of handling http requests, i.e. requests.session()
        """
        self._request_handler: t.Type[RequestHandler] = request_handler

    def process_request(self,
                        method: str,
                        path: str,
                        extra_params: t.Optional[RequestParams] = None,
                        json: t.Optional[RequestParams] = None,
                        many: bool = False,
                        response_class: t.Optional[BaseModel] = None) -> t.Union[t.Any, t.List[t.Any]]:
        """
        Performs a HTTP Request depending on the given method and processes accordingly the Response

        :param method: one of GET, POST, PUT, DELETE
        :param path: the URI of the request
        :param extra_params: dict, list of tuples or bytes to send in the query string for the Request
        :param json: A JSON serializable Python object to send in the body of the Request
        :param many: indicates whether the response is a list of objects or not
        :param response_class: the Python class to be used for deserialization of the Response data
        :return: response_class or list of response class or dict or list of dict
        :raises: APIError
        """

        if method == 'GET':
            response = self._request_handler.get(path, params=extra_params or {}, json=json)
        elif method == 'POST':
            response = self._request_handler.post(path, json=json)
        elif method == 'DELETE':
            response = self._request_handler.delete(path, json=json)
        elif method == 'PUT':
            response = self._request_handler.put(path, json=json)
        else:
            raise NotImplementedError(f"Method {method} is not implemented")

        if response.status_code not in [200, 201, 204]:
            raise APIError.from_response(response)

        result = response.json() if len(response.content) > 0 else None

        if response_class and result:
            if many:
                result = (response_class.deserialize(r) for r in result)
            else:
                result = response_class.deserialize(result)

        return list(result) if many and result else result
