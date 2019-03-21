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

from base import Requestor
from base.errors import APIError
from tests._base.utils import TestModel

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('method', [None, 'wrong', 'get', 'gets'])
def test_do_request__wrong_method__raises_notimplementederror(method):
    requestor = Requestor(request_handler=Mock())

    with pytest.raises(NotImplementedError) as e:
        requestor._do_request(method, 'path', {}, {})
    assert f"Method {method} is not implemented" == str(e.value)


@pytest.mark.parametrize('method', ['GET', 'POST', 'PUT', 'DELETE'])
def test_do_request__corrent_method_is_called(method):
    mock_request_handler = Mock()
    mock_request_handler.get = Mock()
    mock_request_handler.post = Mock()
    mock_request_handler.put = Mock()
    mock_request_handler.delete = Mock()

    requestor = Requestor(request_handler=mock_request_handler)

    requestor._do_request(method, 'path', {}, {})

    called_method = getattr(mock_request_handler, method.lower())

    called_method.assert_called_once()


@pytest.mark.parametrize('status_code, should_raise', [
    (200, False),
    (201, False),
    (204, False),
    (400, True),
    (401, True),
    (403, True),
    (404, True),
    (500, True),
])
def test_process_response__error_status_code_should_raise__normal_status_code_should_not(status_code, should_raise):
    data = {'a': 1}
    response = Mock()
    response.status_code = status_code
    response.content = data
    response.json = Mock(return_value=data)

    requestor = Requestor(request_handler=Mock())

    if should_raise:
        with pytest.raises(APIError):
            requestor._process_response(response, response_class=None, many=False)
    else:
        requestor._process_response(response, response_class=None, many=False)


@pytest.mark.parametrize('data, many, expected_object', [
    ({'a': 1, 'b': 2}, False, TestModel(a=1, b=2)),
    ([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], True, [TestModel(a=1, b=2), TestModel(a=3, b=4)])
])
def test_process_response__result_is_converted_to_response_class_object(data, many, expected_object):
    response = Mock()
    response.status_code = 200
    response.content = data
    response.json = Mock(return_value=data)

    requestor = Requestor(request_handler=Mock())

    processed_response = requestor._process_response(response, TestModel, many)

    assert expected_object == processed_response
