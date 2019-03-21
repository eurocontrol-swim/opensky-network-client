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
from unittest.mock import Mock

import pytest

from base.request_handler import RequestHandler

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('host, https, expected_base_url', [
    ('some_host.com', False, 'http://some_host.com/'),
    ('some_host.com', True, 'https://some_host.com/'),
])
def test_base_url(host, https, expected_base_url):
    request_handler = RequestHandler(host, https=https)

    assert expected_base_url == request_handler._base_url


@pytest.mark.parametrize('method', ['get', 'put', 'post', 'delete'])
@pytest.mark.parametrize('host', ['some_host.com'])
@pytest.mark.parametrize('https, endpoint_url, expected_url', [
    (False, 'endpoint/', 'http://some_host.com/endpoint/'),
    (False, 'endpoint', 'http://some_host.com/endpoint'),
    (True, 'endpoint', 'https://some_host.com/endpoint'),
    (True, 'endpoint/', 'https://some_host.com/endpoint/'),
])
def test_get_delete_methods__correct_url_was_used(method, host, https, endpoint_url, expected_url):
    mock_client = Mock()
    mock_method = Mock(return_value='data')
    setattr(mock_client, method, mock_method)

    handler_maker = Mock(return_value=mock_client)

    client = RequestHandler(host, https=https, timeout=10, request_handler_maker=handler_maker)

    response = getattr(client, method)(endpoint_url, **dict())

    url = mock_method.call_args[0][0]
    assert expected_url == url
    # mock_method.assert_called_once_with(expected_url, params=None, timeout=timeout)

    assert response == "data"


@pytest.mark.parametrize('method', ['post', 'put'])
@pytest.mark.parametrize('endpoint_url', ['endpoint/'])
@pytest.mark.parametrize("data, json, kwargs", [
    ("", "{}", {}),
    ("", "{data}", {'a': 1}),
    ("", "{}", {'a': 1, 'b': 2}),
    ("something", "{}", {}),
    ("something", "{data}", {'a': 1}),
    ("something", "{}", {'a': 1, 'b': 2}),
    (None, "{}", {}),
    (None, "{data}", {'a': 1}),
    (None, "{}", {'a': 1, 'b': 2}),
    ("something", None, {}),
    ("something", None, {'a': 1}),
    ("something", None, {'a': 1, 'b': 1}),
])
def test_post_put_extra_parameters(method, endpoint_url, data, json, kwargs):
    mock_client = Mock()
    mock_method = Mock(return_value="data")
    setattr(mock_client, method, mock_method)

    handler_maker = Mock(return_value=mock_client)

    host = "some_host.com"
    expected_url = f"http://{host}/{endpoint_url}"

    client = RequestHandler(host, https=False, request_handler_maker=handler_maker, timeout=10)

    response = getattr(client, method)(endpoint_url, data=data, json=json, **kwargs)

    getattr(mock_client, method).assert_called_once_with(expected_url, data=data, json=json, timeout=10, **kwargs)

    assert response == "data"


@pytest.mark.parametrize('method', ['get', 'delete'])
@pytest.mark.parametrize("endpoint_url, params, kwargs", [
    ("endpoint/", {}, {}),
    ("endpoint/", {'a': 1}, {}),
    ("endpoint/", {}, {'a': 1}),
    ("endpoint/", {'b': 2}, {'a': 1}),
])
def test_get_delete__extra_parameters(method, endpoint_url, params, kwargs):
    mock_client = Mock()
    mock_method = Mock(return_value="data")
    setattr(mock_client, method, mock_method)

    handler_maker = Mock(return_value=mock_client)

    host = "some_host.com"
    expected_url = f"http://{host}/{endpoint_url}"

    client = RequestHandler(host, https=False, request_handler_maker=handler_maker, timeout=10)

    response = getattr(client, method)(endpoint_url, params=params, **kwargs)

    getattr(mock_client, method).assert_called_once_with(expected_url, params=params, timeout=10, **kwargs)

    assert response == "data"
