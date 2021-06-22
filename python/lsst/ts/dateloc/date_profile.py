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
import palpy

from datetime import datetime, timedelta

__all__ = ["DateProfile"]


class DateProfile(object):
    """This class handles calculating the Modified Julian Date and the Local
    Sidereal Time for the internal timestamp and location coordinates.

    Parameters
    ----------
    timestamp : float
        The UTC timestamp for a given date/time.
    location : lsst.ts.dateloc.ObservatoryLocation
        The location site information instance.
    """

    SECONDS_IN_HOUR = 60.0 * 60.0

    def __init__(self, timestamp, location):
        self.location = location
        self.update(timestamp)

    def __call__(self, timestamp):
        """Modified Julian Date and Local Sidereal Time from instance.

        Parameters
        ----------
        timestamp : float
            The UTC timestamp to get the MJD and LST for.

        Returns
        -------
        (float, float)
            A tuple of the Modified Julian Date and Local Sidereal Time
            (radians).
        """
        self.update(timestamp)
        return (self.mjd, self.lst_rad)

    def __get_timestamp(self, dt):
        """Get timestamp

        Parameters
        ----------
        dt : datetime
            Date, in `datetime` format, to convert to timestamp.

        Returns
        -------
        float
            Return a timestamp from the datetime instance.
        """
        return (dt - datetime(1970, 1, 1)).total_seconds()

    @property
    def lst_rad(self):
        """Local sidereal time (in radians).

        Returns
        -------
        value : float
            Local Sidereal Time (radians) for the internal timestamp.
        """
        value = palpy.gmst(self.mjd) + self.location.longitude_rad
        if value < 0.0:
            value += 2.0 * math.pi
        return value

    @property
    def mjd(self):
        """Modified Julian Date for the internal timestamp.

        Returns
        -------
        mjd : float
            Modified Julian Date for the internal timestamp.
        """
        mjd = palpy.caldj(
            self.current_dt.year, self.current_dt.month, self.current_dt.day
        )
        mjd += (
            (self.current_dt.hour / 24.0)
            + (self.current_dt.minute / 1440.0)
            + (self.current_dt.second / 86400.0)
        )
        return mjd

    def midnight_timestamp(self):
        """Return the current midnight timestamp.

        Returns
        -------
        float
            The UTC timestamp of midnight for the current date.
        """
        midnight_dt = datetime(
            self.current_dt.year, self.current_dt.month, self.current_dt.day
        )
        return self.__get_timestamp(midnight_dt)

    def next_midnight_timestamp(self):
        """Return the next midnight timestamp.

        Returns
        -------
        float
            UTC timestamp of midnight for the next day after current date.
        """
        midnight_dt = datetime(
            self.current_dt.year, self.current_dt.month, self.current_dt.day
        )
        midnight_dt += timedelta(**{"days": 1})
        return self.__get_timestamp(midnight_dt)

    def previous_midnight_timestamp(self):
        """Return the previous midnight timestamp.

        Returns
        -------
        float
            UTC timestamp of midnight for the next day before current date.
        """
        midnight_dt = datetime(
            self.current_dt.year, self.current_dt.month, self.current_dt.day
        )
        midnight_dt -= timedelta(**{"days": 1})
        return self.__get_timestamp(midnight_dt)

    def update(self, timestamp):
        """Change the internal timestamp to requested one.

        Parameters
        ----------
        timestamp : float
            The UTC timestamp to update the internal timestamp to.
        """
        self.timestamp = timestamp
        self.current_dt = datetime.utcfromtimestamp(self.timestamp)
