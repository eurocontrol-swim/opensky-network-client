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
import pytest

from opensky_network_client.models import StateVector, States, PositionSource, FlightArrival, FlightDeparture

__author__ = "EUROCONTROL (SWIM)"

@pytest.mark.parametrize('state_vector_list, expected_state_vector', [
    (["3c6444", "DLH9LF ", "Germany", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26, 4.55, None,
      9547.86, "1000", False, PositionSource.ASD_B],
     StateVector("3c6444", "DLH9LF ", "Germany", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26,
                 4.55, None, 9547.86, "1000", False, PositionSource.ASD_B)
     )
])
def test_state_vector__from_list(state_vector_list, expected_state_vector):
    state_vector = StateVector.from_list(state_vector_list)

    assert expected_state_vector == state_vector


@pytest.mark.parametrize('states_dict, expected_states', [
(
    {
        "time": 1458564121,
        "states": [
            ["3c6444", "DLH9LF ", "Germany", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26,
             4.55, None, 9547.86, "1000", False, PositionSource.ASD_B],
            ["3c6444", "DLH9LF ", "Greece", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False, 232.88, 98.26,
             4.55, None, 9547.86, "1000", False, PositionSource.ASD_B]
        ]
    },
    States(
        time_in_sec=1458564121,
        states=[StateVector("3c6444", "DLH9LF ", "Germany", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False,
                            232.88, 98.26, 4.55, None, 9547.86, "1000", False, PositionSource.ASD_B),
                StateVector("3c6444", "DLH9LF ", "Greece", 1458564120, 1458564120, 6.1546, 50.1964, 9639.3, False,
                            232.88, 98.26, 4.55, None, 9547.86, "1000", False, PositionSource.ASD_B)
                ]
    )
)
])
def test_states__from_dict(states_dict, expected_states):
    states = States.from_dict(states_dict)

    assert expected_states.time_in_sec == states.time_in_sec


@pytest.mark.parametrize('flight_arrival_dict, expected_flight_arrival', [
    (
        {
            "icao24": "0101be",
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
        },
        FlightArrival(
            icao24="0101be",
            first_seen=1517220729,
            est_departure_airport=None,
            last_seen=1517230737,
            est_arrival_airport="EDDF",
            callsign="MSR785 ",
            est_departure_airport_horiz_distance=None,
            est_departure_airport_vert_distance=None,
            est_arrival_airport_horiz_distance=1593,
            est_arrival_airport_vert_distance=95,
            departure_airport_candidates_count=0,
            arrival_airport_candidates_count=2
        )
    )
])
def test_flight_arrival__from_dict(flight_arrival_dict, expected_flight_arrival):
    flight_arrival = FlightArrival.from_dict(flight_arrival_dict)

    assert expected_flight_arrival == flight_arrival


@pytest.mark.parametrize('flight_departure_dict, expected_flight_departure', [
    (
        {
            "icao24": "0101be",
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
        },
        FlightDeparture(
            icao24="0101be",
            first_seen=1517220729,
            est_departure_airport=None,
            last_seen=1517230737,
            est_arrival_airport="EDDF",
            callsign="MSR785 ",
            est_departure_airport_horiz_distance=None,
            est_departure_airport_vert_distance=None,
            est_arrival_airport_horiz_distance=1593,
            est_arrival_airport_vert_distance=95,
            departure_airport_candidates_count=0,
            arrival_airport_candidates_count=2
        )
    )
])
def test_flight_departure__from_dict(flight_departure_dict, expected_flight_departure):
    flight_departure = FlightDeparture.from_dict(flight_departure_dict)

    assert expected_flight_departure == flight_departure