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
from typing import Optional, Type

from base import RequestHandler, RestClientType

__author__ = "EUROCONTROL (SWIM)"


class ClientFactory:
    """
    """
    @classmethod
    def create(cls,
               host: str,
               https: bool = True,
               timeout: int = None,
               username: Optional[str] = None,
               password: Optional[str] = None,
               **kwargs: str) -> Type[RestClientType]:
        """
        To be used from a REST client class that inherits from ClientFactory. The returned class will be an instance of
        the REST client class.

        :param host: the host provider of the API
        :param https: indicates whether the host serves over TSL or not
        :param username: username for basic authentication
        :param password: password for basic authentication
        :param timeout: How many seconds to wait for the server to send data before giving up
        :param kwargs: optional arguments
        :return: an instance of a REST client that will inherit from ClientFactory
        """
        auth = (username, password) if username and password else None

        request_handler = RequestHandler(host=host, https=https, timeout=timeout, auth=auth)

        return cls(request_handler, **kwargs)
