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
import enum
from datetime import datetime

__author__ = "EUROCONTROL (SWIM)"


class Comparable:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.__dict__ == self.__dict__

    def __ne__(self, other):
        return not other == self


class PositionSource(enum.Enum):
    ASD_B = 0
    ASTERIX = 1
    MLAT = 2
    FLARM = 3


class StateVector(Comparable):

    def __init__(self, icao24, callsign, origin_country, time_position_in_sec, last_contact_in_sec, longitude, latitude,
                 baro_altitude_in_m, on_ground, velocity_in_mi_per_sec, heading, vertical_rate_in_m_per_s, sensors,
                 geo_altitude_in_m, squawk, spi, position_source):
        """
        Represents the state of a vehicle at a particular time

        :param icao24: ICAO24 address of the transmitter in hex string representation.
        :type icao24: str
        :param callsign: callsign of the vehicle. Can be None if no callsign has been received.
        :type callsign: str or None
        :param origin_country: inferred through the ICAO24 address
        :type origin_country: str
        :param time_position_in_sec: seconds since epoch of last position report. Can be None if there was no position
                                     report received by OpenSky within 15s before.
        :type time_position_in_sec: int or None
        :param last_contact_in_sec: seconds since epoch of last received message from this transponder
        :type last_contact_in_sec: int
        :param longitude: in ellipsoidal coordinates (WGS-84) and degrees. Can be None
        :type longitude: float or None
        :param latitude: in ellipsoidal coordinates (WGS-84) and degrees. Can be None
        :type latitude: float or None
        :param baro_altitude_in_m: barometric altitude in meters. Can be None
        :type baro_altitude_in_m: float or None
        :param on_ground: true if aircraft is on ground (sends ADS-B surface position reports).
        :type on_ground: bool
        :param velocity_in_mi_per_sec: over ground in m/s. Can be None if information not present
        :type velocity_in_mi_per_sec: float or None
        :param heading: in decimal degrees (0 is north). Can be None if information not present.
        :type heading: float or None
        :param vertical_rate_in_m_per_s: in m/s, incline is positive, decline negative. Can be None if information not
                                         present.
        :type vertical_rate_in_m_per_s: float or None
        :param sensors: serial numbers of sensors which received messages from the vehicle within the validity period of
                        this state vector. Can be None if no filtering for sensor has been requested.
        :type sensors: str or None
        :param geo_altitude_in_m: geometric altitude in meters. Can be None
        :type geo_altitude_in_m: float or None
        :param squawk: transponder code aka Squawk. Can be None
        :type squawk: str or None
        :param spi: special purpose indicator
        :type spi: bool
        :param position_source: origin of this state's position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM
        :type position_source: PositionSource
        """
        self.icao24 = icao24,
        self.callsign = callsign,
        self.origin_country = origin_country,
        self.time_position_in_sec = time_position_in_sec,
        self.last_contact_in_sec = last_contact_in_sec,
        self.longitude = longitude,
        self.latitude = latitude,
        self.baro_altitude_in_m = baro_altitude_in_m,
        self.on_ground = on_ground,
        self.velocity_in_mi_per_sec = velocity_in_mi_per_sec,
        self.heading = heading,
        self.vertical_rate_in_m_per_s = vertical_rate_in_m_per_s,
        self.sensors = sensors,
        self.geo_altitude_in_m = geo_altitude_in_m,
        self.squawk = squawk,
        self.spi = spi,
        self.position_source = position_source

    @classmethod
    def from_list(cls, state_vector_list):
        """
        :param state_vector_list:
        :type state_vector_list: list
        :return:
        :rtype: StateVector
        """
        return cls(*state_vector_list)


class States(Comparable):

    def __init__(self, time_in_sec, states):
        """
        Represents the state of the airspace as seen by OpenSky at a particular time.
        :param time_in_sec: time since Unix epoch
        :type time_in_sec: int
        :param states:
        :type states:
        """
        self.time_in_sec = time_in_sec
        self.states = states

        self.time = datetime.fromtimestamp(time_in_sec)

    @classmethod
    def from_dict(cls, states_dict):
        return cls(
            time_in_sec=states_dict['time'],
            states=[StateVector.from_list(state_vector_list) for state_vector_list in states_dict['states']]
                if states_dict['states'] is not None else []
        )


class FlightConnection(Comparable):

    def __init__(self, icao24, first_seen, est_departure_airport, last_seen, est_arrival_airport, callsign,
                 est_departure_airport_horiz_distance, est_departure_airport_vert_distance,
                 est_arrival_airport_horiz_distance, est_arrival_airport_vert_distance,
                 departure_airport_candidates_count, arrival_airport_candidates_count):
        """
        Represents a flight departure or arrival for a certain airport.

        :param icao24: Unique ICAO 24-bit address of the transponder in hex string representation. All letters are lower
                       case.
        :type icao24: str
        :param first_seen: Estimated time of departure for the flight as Unix time (seconds since epoch).
        :type first_seen: int
        :param est_departure_airport: ICAO code of the estimated departure airport. Can be null if the airport could not
                                      be identified.
        :type est_departure_airport: str or None
        :param last_seen: Estimated time of arrival for the flight as Unix time (seconds since epoch)
        :type last_seen: int
        :param est_arrival_airport: ICAO code of the estimated arrival airport. Can be null if the airport could not be
                                    identified.
        :type est_arrival_airport: str or None
        :param callsign: Callsign of the vehicle (8 chars). Can be null if no callsign has been received. If the vehicle
                         transmits multiple callsigns during the flight, we take the one seen most frequently
        :type callsign: str or None
        :param est_departure_airport_horiz_distance: Horizontal distance of the last received airborne position to the
                                                     estimated departure airport in meters
        :type est_departure_airport_horiz_distance: int or None
        :param est_departure_airport_vert_distance: Vertical distance of the last received airborne position to the
                                                    estimated departure airport in meters
        :type est_departure_airport_vert_distance: int or None
        :param est_arrival_airport_horiz_distance: Horizontal distance of the last received airborne position to the
                                                   estimated arrival airport in meters
        :type est_arrival_airport_horiz_distance: int
        :param est_arrival_airport_vert_distance: Vertical distance of the last received airborne position to the
                                                  estimated arrival airport in meters
        :type est_arrival_airport_vert_distance: int
        :param departure_airport_candidates_count: Number of other possible departure airports. These are airports in
                                                   short distance to estDepartureAirport.
        :type departure_airport_candidates_count: int
        :param arrival_airport_candidates_count: Number of other possible departure airports. These are airports in short
                                                 distance to estArrivalAirport.
        :type arrival_airport_candidates_count: int
        """
        self.icao24 = icao24
        self.first_seen = first_seen
        self.est_departure_airport = est_departure_airport
        self.last_seen = last_seen
        self.est_arrival_airport = est_arrival_airport
        self.callsign = callsign
        self.est_departure_airport_horiz_distance = est_departure_airport_horiz_distance
        self.est_departure_airport_vert_distance = est_departure_airport_vert_distance
        self.est_arrival_airport_horiz_distance = est_arrival_airport_horiz_distance
        self.est_arrival_airport_vert_distance = est_arrival_airport_vert_distance
        self.departure_airport_candidates_count = departure_airport_candidates_count
        self.arrival_airport_candidates_count = arrival_airport_candidates_count

    @classmethod
    def from_dict(cls, arrival_dict):
        return cls(
            icao24=arrival_dict["icao24"],
            first_seen=arrival_dict["firstSeen"],
            est_departure_airport=arrival_dict["estDepartureAirport"],
            last_seen=arrival_dict["lastSeen"],
            est_arrival_airport=arrival_dict["estArrivalAirport"],
            callsign=arrival_dict["callsign"],
            est_departure_airport_horiz_distance=arrival_dict["estDepartureAirportHorizDistance"],
            est_departure_airport_vert_distance=arrival_dict["estDepartureAirportVertDistance"],
            est_arrival_airport_horiz_distance=arrival_dict["estArrivalAirportHorizDistance"],
            est_arrival_airport_vert_distance=arrival_dict["estArrivalAirportVertDistance"],
            departure_airport_candidates_count=arrival_dict["departureAirportCandidatesCount"],
            arrival_airport_candidates_count=arrival_dict["arrivalAirportCandidatesCount"]
        )


class FlightArrival(FlightConnection):
    """Represents a flight arrival for a certain airport."""


class FlightDeparture(FlightConnection):
    """Represents a flight departure for a certain airport."""
