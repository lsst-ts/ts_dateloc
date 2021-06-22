# This file is part of ts_dateloc.
#
# Developed for the Vera Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import math

import rubin_sim.utils as simsUtils

__all__ = ["ObservatoryLocation"]


class ObservatoryLocation(object):
    """Class for the observatory location.

    This class handles keeping the necessary information for the observatory's
    location.

    Attributes
    ----------
    height : float
        The elevation of the observatory in meters.
    latitude_rad : float
        The latitude of the observatory in radians.
    longitude_rad : float
        The longitude of the observatory in radians.
    """

    def __init__(self, latitude_rad=0.0, longitude_rad=0.0, height=0.0):
        """Initialize the class.

        Parameters
        ----------
        latitude_rad : float
            The latitude (radians) position of the observatory.
        longitude_rad : float
            The longitude (radians) position of the observatory.
        height : float
            The elevation (meters) of the observatory.
        """
        self.height = height
        self.latitude_rad = latitude_rad
        self.longitude_rad = longitude_rad

    @classmethod
    def get_configure_dict(cls):
        """Get the configuration dictionary for the observatory location.

        Returns
        -------
        dict
            The configuration dictionary for the observatory location.
        """
        lsst = simsUtils.Site(name="LSST")
        conf_dict = {
            "obs_site": {
                "latitude": lsst.latitude,
                "longitude": lsst.longitude,
                "height": lsst.height,
            }
        }
        return conf_dict

    @property
    def latitude(self):
        """float: Return the observatory's latitude in degrees."""
        return math.degrees(self.latitude_rad)

    @property
    def longitude(self):
        """float: Return the observatory's longitude in degrees."""
        return math.degrees(self.longitude_rad)

    def configure(self, location_confdict):
        """Configure the observatory information via a dictionary.

        This function requires a simple dictionary for the observatory
        information. The dictionary needs to look like this:

        {'obs_site': {'latitude': 0.0, 'longitude': 0.0, 'height': 0.0}}

        The numerical values should be replaced with proper values in the
        class's expected units. The latitude and longitude can be specified in
        degrees in the dictionary and they will be converted internally.

        Parameters
        ----------
        location_confdict : dict
            The observatory information.
        """
        self.latitude_rad = math.radians(location_confdict["obs_site"]["latitude"])
        self.longitude_rad = math.radians(location_confdict["obs_site"]["longitude"])
        self.height = location_confdict["obs_site"]["height"]

    def for_lsst(self):
        """A convenience function to set the observatory location for LSST."""
        lsst = simsUtils.Site(name="LSST")
        self.latitude_rad = math.radians(lsst.latitude)
        self.longitude_rad = math.radians(lsst.longitude)
        self.height = lsst.height

    def reconfigure(self, latitude_rad, longitude_rad, height):
        """Override the current observatory information.

        Parameters
        ----------
        latitude_rad : float
            The latitude (radians) position of the observatory.
        longitude_rad : float
            The longitude (radians) position of the observatory.
        height : float
            The elevation (meters) of the observatory.
        """
        self.latitude_rad = latitude_rad
        self.longitude_rad = longitude_rad
        self.height = height
