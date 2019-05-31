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
from opensky_network_client.models import PositionSource, StateVector, States, FlightConnection, Airport

__author__ = "EUROCONTROL (SWIM)"


def make_states():
    states_dict = {
            "time": 1458564121,
            "states": [
                ["3c6444", "DLH9LF ", "Germany", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26,
                 4.55, None, 9547.86, "1000", False, PositionSource.ASD_B],
                ["4b1806", "DLH9LF ", "Greece", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26,
                 4.55, None, 9547.86, "1000", False, PositionSource.ASD_B]
            ]
        }

    states = States.from_json(states_dict)

    return states_dict, states


def make_flight_connection(icao24=None):
    flight_connection_dict = {
            "icao24": icao24 or "0101be",
            "firstSeen": 1517220729,
            "estDepartureAirport": None,
            "lastSeen": 1517230737,
            "estArrivalAirport": "EDDF",
            "callsign": "MSR785 ",
            "estDepartureAirportHorizDistance": None,
            "estDepartureAirportVertDistance": None,
            "estArrivalAirportHorizDistance": 1593,
            "estArrivalAirportVertDistance": 95,
            "departureAirportCandidatesCount": 0,
            "arrivalAirportCandidatesCount": 2
        }

    flight_connection = FlightConnection.from_json(flight_connection_dict)

    return flight_connection_dict, flight_connection


def make_airport():
    airport_dict = {
        'icao': 'UUEE',
        'iata': 'SVO',
        'name': 'Sheremetyevo International Airport',
        'city': None,
        'type': None,
        'position': {
            'longitude': 37.4146,
            'latitude': 55.972599,
            'altitude': 189.5856,
            'reasonable': True,
        },
        'continent': 'EU',
        'country': 'RU',
        'region': 'RU-MOS',
        'municipality': 'Moscow',
        'gpsCode': 'UUEE',
        'homepage': 'http://www.svo.aero/en/',
        'wikipedia': 'http://en.wikipedia.org/wiki/Sheremetyevo_International_Airport'
    }

    airport = Airport.from_json(airport_dict)

    return airport_dict, airport


def make_flight_connection_list():
    flight_connection_dict1, flight_connection1 = make_flight_connection()
    flight_connection_dict2, flight_connection2 = make_flight_connection(icao24="0101be")

    return [flight_connection_dict1, flight_connection_dict2], [flight_connection1, flight_connection2]
