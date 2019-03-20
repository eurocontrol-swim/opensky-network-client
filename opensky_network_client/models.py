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
from __future__ import annotations
import enum
from datetime import datetime
from typing import Optional, List, TypeVar, Dict

from base import BaseModel

__author__ = "EUROCONTROL (SWIM)"


StateVectorData = TypeVar('StateVectorData', str, bool, int, float)
FlightConnectionData = TypeVar('FlightConnectionData', str, int)


class PositionSource(enum.Enum):
    ASD_B = 0
    ASTERIX = 1
    MLAT = 2
    FLARM = 3


class StateVector(BaseModel):

    def __init__(self,
                 icao24: str,
                 callsign: Optional[str],
                 origin_country: str,
                 time_position_in_sec: Optional[int],
                 last_contact_in_sec: int,
                 longitude: Optional[float],
                 latitude: Optional[float],
                 baro_altitude_in_m: Optional[float],
                 on_ground: bool,
                 velocity_in_mi_per_sec: Optional[float],
                 heading: Optional[float],
                 vertical_rate_in_m_per_s: Optional[float],
                 sensors: Optional[str],
                 geo_altitude_in_m: Optional[float],
                 squawk: Optional[str],
                 spi: bool,
                 position_source: PositionSource) -> None:
        """
        Represents the state of a vehicle at a particular time

        :param icao24: ICAO24 address of the transmitter in hex string representation.
        :param callsign: callsign of the vehicle. Can be None if no callsign has been received.
        :param origin_country: inferred through the ICAO24 address
        :param time_position_in_sec: seconds since epoch of last position report. Can be None if there was no position
                                     report received by OpenSky within 15s before.
        :param last_contact_in_sec: seconds since epoch of last received message from this transponder
        :param longitude: in ellipsoidal coordinates (WGS-84) and degrees. Can be None
        :param latitude: in ellipsoidal coordinates (WGS-84) and degrees. Can be None
        :param baro_altitude_in_m: barometric altitude in meters. Can be None
        :param on_ground: true if aircraft is on ground (sends ADS-B surface position reports).
        :param velocity_in_mi_per_sec: over ground in m/s. Can be None if information not present
        :param heading: in decimal degrees (0 is north). Can be None if information not present.
        :param vertical_rate_in_m_per_s: in m/s, incline is positive, decline negative. Can be None if information not
                                         present.
        :param sensors: serial numbers of sensors which received messages from the vehicle within the validity period of
                        this state vector. Can be None if no filtering for sensor has been requested.
        :param geo_altitude_in_m: geometric altitude in meters. Can be None
        :param squawk: transponder code aka Squawk. Can be None
        :param spi: special purpose indicator
        :param position_source: origin of this state's position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM
        """
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.time_position_in_sec = time_position_in_sec
        self.last_contact_in_sec = last_contact_in_sec
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude_in_m = baro_altitude_in_m
        self.on_ground = on_ground
        self.velocity_in_mi_per_sec = velocity_in_mi_per_sec
        self.heading = heading
        self.vertical_rate_in_m_per_s = vertical_rate_in_m_per_s
        self.sensors = sensors
        self.geo_altitude_in_m = geo_altitude_in_m
        self.squawk = squawk
        self.spi = spi
        self.position_source = position_source

    @classmethod
    def deserialize(cls, state_vector_list: List[StateVectorData]) -> StateVector:
        """
        :param state_vector_list:
        :return:
        """
        return cls(*state_vector_list)


class States(BaseModel):

    def __init__(self, time_in_sec: int, states: List[StateVector]) -> None:
        """
        Represents the state of the airspace as seen by OpenSky at a particular time.
        :param time_in_sec: time since Unix epoch
        :param states:
        """
        self.time_in_sec = time_in_sec
        self.states = states

        self.time = datetime.fromtimestamp(time_in_sec)

    @classmethod
    def deserialize(cls, states_dict: Dict[str, StateVectorData]) -> States:
        return cls(
            time_in_sec=states_dict['time'],
            states=[StateVector.deserialize(state_vector_list) for state_vector_list in states_dict['states']]
        )


class FlightConnection(BaseModel):

    def __init__(self,
                 icao24: str,
                 first_seen: int,
                 est_departure_airport: Optional[str],
                 last_seen: int,
                 est_arrival_airport: Optional[str],
                 callsign: Optional[str],
                 est_departure_airport_horiz_distance: Optional[int],
                 est_departure_airport_vert_distance: Optional[int],
                 est_arrival_airport_horiz_distance: int,
                 est_arrival_airport_vert_distance: int,
                 departure_airport_candidates_count: int,
                 arrival_airport_candidates_count: int) -> None:
        """
        Represents a flight departure or arrival for a certain airport.

        :param icao24: Unique ICAO 24-bit address of the transponder in hex string representation. All letters are lower
                       case.
        :param first_seen: Estimated time of departure for the flight as Unix time (seconds since epoch).
        :param est_departure_airport: ICAO code of the estimated departure airport. Can be null if the airport could not
                                      be identified.
        :param last_seen: Estimated time of arrival for the flight as Unix time (seconds since epoch)
        :param est_arrival_airport: ICAO code of the estimated arrival airport. Can be null if the airport could not be
                                    identified.
        :param callsign: Callsign of the vehicle (8 chars). Can be null if no callsign has been received. If the vehicle
                         transmits multiple callsigns during the flight, we take the one seen most frequently
        :param est_departure_airport_horiz_distance: Horizontal distance of the last received airborne position to the
                                                     estimated departure airport in meters
        :param est_departure_airport_vert_distance: Vertical distance of the last received airborne position to the
                                                    estimated departure airport in meters
        :param est_arrival_airport_horiz_distance: Horizontal distance of the last received airborne position to the
                                                   estimated arrival airport in meters
        :param est_arrival_airport_vert_distance: Vertical distance of the last received airborne position to the
                                                  estimated arrival airport in meters
        :param departure_airport_candidates_count: Number of other possible departure airports. These are airports in
                                                   short distance to estDepartureAirport.
        :param arrival_airport_candidates_count: Number of other possible departure airports. These are airports in
                                                 short distance to estArrivalAirport.
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
    def deserialize(cls, arrival_dict: Dict[str: FlightConnectionData]) -> object:
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


class BoundingBox(BaseModel):

    def __init__(self, lamin: float, lamax: float, lomin: float, lomax: float) -> None:
        """
        Represents a bounding box of WGS84 coordinates

        :param lamin: lower bound for the latitude in decimal degrees
        :param lamax: upper bound for the latitude in decimal degrees
        :param lomin: lower bound for the longitude in decimal degrees
        :param lomax: upper bound for the longitude in decimal degrees
        """
        self.lamin = self._validate_lat(lamin)
        self.lamax = self._validate_lat(lamax)
        self.lomin = self._validate_lon(lomin)
        self.lomax = self._validate_lon(lomax)

    def serialize(self) -> Dict[str, float]:
        return {
            "lamin": self.lamin,
            "lamax": self.lamax,
            "lomin": self.lomin,
            "lomax": self.lomax
        }

    @staticmethod
    def _validate_lat(lat):
        if lat < -90 or lat > 90:
            raise ValueError(f"Invalid latitude {lat}. Must be in [-90, 90]")

        return lat

    @staticmethod
    def _validate_lon(lon):
        if lon < -180 or lon > 180:
            raise ValueError(f"Invalid longitude {lon}. Must be in [-180, 180]")

        return lon
