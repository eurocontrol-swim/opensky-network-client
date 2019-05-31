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
from datetime import datetime
from unittest.mock import Mock

import pytest

from rest_client.errors import APIError
from opensky_network_client.models import BoundingBox
from opensky_network_client.opensky_network import OpenskyNetworkClient
from tests.utils import make_states, make_flight_connection_list, make_airport

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('error_code', [400, 401, 403, 404, 500])
def test_get_states__http_error_code__raises_api_error(error_code):
    response = Mock()
    response.status_code = error_code

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    with pytest.raises(APIError):
        client.get_states()


def test_get_states__states_object_is_returned():
    states_dict, expected_states = make_states()

    response = Mock()
    response.status_code = 200
    response.content = states_dict
    response.json = Mock(return_value=states_dict)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'timestamp': 1517230800,
        'icao24': '3c4ad0',
        'bbox': BoundingBox(lamin=85.453421, lamax=80.545676, lomin=50.454257, lomax=45.871253)
    }
    states = client.get_states(**params)

    assert expected_states == states

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['time'] == params['timestamp']
    assert call_args['params']['icao24'] == params['icao24']
    assert call_args['params']['lamin'] == params['bbox'].lamin
    assert call_args['params']['lamax'] == params['bbox'].lamax
    assert call_args['params']['lomin'] == params['bbox'].lomin
    assert call_args['params']['lomax'] == params['bbox'].lomax


def test_get_states__json_true__states_dict_is_returned():
    states_dict, _ = make_states()

    response = Mock()
    response.status_code = 200
    response.content = states_dict
    response.json = Mock(return_value=states_dict)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'timestamp': 1517230800,
        'icao24': '3c4ad0',
        'bbox': BoundingBox(lamin=85.453421, lamax=80.545676, lomin=50.454257, lomax=45.871253),
        'json': True
    }
    states = client.get_states(**params)

    assert states_dict == states

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['time'] == params['timestamp']
    assert call_args['params']['icao24'] == params['icao24']
    assert call_args['params']['lamin'] == params['bbox'].lamin
    assert call_args['params']['lamax'] == params['bbox'].lamax
    assert call_args['params']['lomin'] == params['bbox'].lomin
    assert call_args['params']['lomax'] == params['bbox'].lomax


def test_get_states__time_is_timestamp__it_is_converted_to_int_and_states_object_is_returned():
    states_dict, expected_states = make_states()

    response = Mock()
    response.status_code = 200
    response.content = states_dict
    response.json = Mock(return_value=states_dict)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    timestamp = datetime.now()
    params = {
        'timestamp': timestamp,
        'icao24': '3c4ad0',
        'bbox': BoundingBox(lamin=85.453421, lamax=80.545676, lomin=50.454257, lomax=45.871253)
    }
    states = client.get_states(**params)

    assert expected_states == states

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['time'] == int(params['timestamp'].timestamp())
    assert call_args['params']['icao24'] == params['icao24']
    assert call_args['params']['lamin'] == params['bbox'].lamin
    assert call_args['params']['lamax'] == params['bbox'].lamax
    assert call_args['params']['lomin'] == params['bbox'].lomin
    assert call_args['params']['lomax'] == params['bbox'].lomax


@pytest.mark.parametrize('error_code', [400, 401, 403, 404, 500])
def test_get_flight_arrivals__http_error_code__raises_api_error(error_code):
    response = Mock()
    response.status_code = error_code

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    with pytest.raises(APIError):
        client.get_flight_arrivals(airport='EDDF', begin=1517227200, end=1517230800)


def test_get_flight_arrivals__flight_arrivals_object_is_returned():
    flight_arrivals_dict_list, expected_flight_arrivals_list = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_arrivals_dict_list
    response.json = Mock(return_value=flight_arrivals_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'airport': 'EDDF',
        'begin': 1517227200,
        'end': 1517230800
    }
    flight_arrivals = client.get_flight_arrivals(**params)

    assert expected_flight_arrivals_list == flight_arrivals

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == params['begin']
    assert call_args['params']['end'] == params['end']


def test_get_flight_arrivals__json_true__flight_arrivals_dict_is_returned():
    flight_arrivals_dict_list, _ = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_arrivals_dict_list
    response.json = Mock(return_value=flight_arrivals_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'airport': 'EDDF',
        'begin': 1517227200,
        'end': 1517230800,
        'json': True
    }
    flight_arrivals = client.get_flight_arrivals(**params)

    assert flight_arrivals_dict_list == flight_arrivals

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == params['begin']
    assert call_args['params']['end'] == params['end']


def test_get_flight_arrivals__with_begin_end_datetime__is_converted_to_int_and_flight_arrivals_object_is_returned():
    flight_arrivals_dict_list, expected_flight_arrivals_list = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_arrivals_dict_list
    response.json = Mock(return_value=flight_arrivals_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    timestamp = datetime.now()
    params = {
        'airport': 'EDDF',
        'begin': timestamp,
        'end': timestamp
    }
    flight_arrivals = client.get_flight_arrivals(**params)

    assert expected_flight_arrivals_list == flight_arrivals

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == int(params['begin'].timestamp())
    assert call_args['params']['end'] == int(params['end'].timestamp())


@pytest.mark.parametrize('error_code', [400, 401, 403, 404, 500])
def test_get_flight_departures__http_error_code__raises_api_error(error_code):
    response = Mock()
    response.status_code = error_code

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    with pytest.raises(APIError):
        client.get_flight_departures(airport='EDDF', begin=1517227200, end=1517230800)


def test_get_flight_departures__flight_departures_object_is_returned():
    flight_departures_dict_list, expected_flight_departures_list = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_departures_dict_list
    response.json = Mock(return_value=flight_departures_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'airport': 'EDDF',
        'begin': 1517227200,
        'end': 1517230800
    }
    flight_departures = client.get_flight_departures(**params)

    assert expected_flight_departures_list == flight_departures

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == params['begin']
    assert call_args['params']['end'] == params['end']


def test_get_flight_departures__json_true__flight_departures_dict_is_returned():
    flight_departures_dict_list, _ = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_departures_dict_list
    response.json = Mock(return_value=flight_departures_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'airport': 'EDDF',
        'begin': 1517227200,
        'end': 1517230800,
        'json': True
    }
    flight_departures = client.get_flight_departures(**params)

    assert flight_departures_dict_list == flight_departures

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == params['begin']
    assert call_args['params']['end'] == params['end']


def test_get_flight_departures__with_begin_end_datetime__is_converted_to_int_and_flight_departures_object_is_returned():
    flight_departures_dict_list, expected_flight_departures_list = make_flight_connection_list()

    response = Mock()
    response.status_code = 200
    response.content = flight_departures_dict_list
    response.json = Mock(return_value=flight_departures_dict_list)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    timestamp = datetime.now()
    params = {
        'airport': 'EDDF',
        'begin': timestamp,
        'end': timestamp
    }
    flight_departures = client.get_flight_departures(**params)

    assert expected_flight_departures_list == flight_departures

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['airport'] == params['airport']
    assert call_args['params']['begin'] == int(params['begin'].timestamp())
    assert call_args['params']['end'] == int(params['end'].timestamp())


@pytest.mark.parametrize('error_code', [400, 401, 403, 404, 500])
def test_get_airport__http_error_code__raises_api_error(error_code):
    response = Mock()
    response.status_code = error_code

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    with pytest.raises(APIError):
        client.get_airport(icao='EDDF')


def test_get_airport__airport_object_is_returned():
    airport_dict, expected_airport = make_airport()

    response = Mock()
    response.status_code = 200
    response.content = airport_dict
    response.json = Mock(return_value=airport_dict)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'icao': 'EDDF'
    }
    airport = client.get_airport(**params)

    assert expected_airport == airport

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['icao'] == params['icao']


def test_get_airport__json_true__airport_dict_is_returned():
    airport_dict, _ = make_airport()

    response = Mock()
    response.status_code = 200
    response.content = airport_dict
    response.json = Mock(return_value=airport_dict)

    request_handler = Mock()
    request_handler.get = Mock(return_value=response)

    client = OpenskyNetworkClient(request_handler=request_handler)

    params = {
        'icao': 'EDDF',
        'json': True
    }
    airport = client.get_airport(**params)

    assert airport_dict == airport

    call_args = request_handler.get.call_args[1]
    assert call_args['params']['icao'] == params['icao']