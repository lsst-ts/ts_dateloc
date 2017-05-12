from __future__ import division
from datetime import datetime, timedelta
import math

import palpy

__all__ = ["DateProfile"]

class DateProfile(object):
    """
    This class handles calculating the Modified Julian Date and the Local Sidereal Time for
    the internal timestamp and location coordinates.
    """

    SECONDS_IN_HOUR = 60.0 * 60.0

    def __init__(self, timestamp, location):
        """Initialize the class.

        Parameters
        ----------
        timestamp : float
            The UTC timestamp for a given date/time.
        location : lsst.ts.dateloc.ObservatoryLocation
            The location site information instance.
        """
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
            A tuple of the Modified Julian Date and Local Sidereal Time (radians).
        """
        self.update(timestamp)
        return (self.mjd, self.lst_rad)

    def __get_timestamp(self, dt):
        """float: Return a timestamp from the datetime instance.
        """
        return (dt - datetime(1970, 1, 1)).total_seconds()

    @property
    def lst_rad(self):
        """float: Return the Local Sidereal Time (radians) for the internal timestamp.
        """
        value = palpy.gmst(self.mjd) + self.location.longitude_rad
        if value < 0.:
            value += 2.0 * math.pi
        return value

    @property
    def mjd(self):
        """float: Return the Modified Julian Date for the internal timestamp.
        """
        mjd = palpy.caldj(self.current_dt.year, self.current_dt.month, self.current_dt.day)
        mjd += (self.current_dt.hour / 24.0) + (self.current_dt.minute / 1440.) + \
               (self.current_dt.second / 86400.)
        return mjd

    def midnight_timestamp(self):
        """float: Return the UTC timestamp of midnight for the current date.
        """
        midnight_dt = datetime(self.current_dt.year, self.current_dt.month, self.current_dt.day)
        return self.__get_timestamp(midnight_dt)

    def next_midnight_timestamp(self):
        """float: Return the UTC timestamp of midnight for the next day after current date.
        """
        midnight_dt = datetime(self.current_dt.year, self.current_dt.month, self.current_dt.day)
        midnight_dt += timedelta(**{"days": 1})
        return self.__get_timestamp(midnight_dt)

    def previous_midnight_timestamp(self):
        """float: Return the UTC timestamp of midnight for the next day before current date.
        """
        midnight_dt = datetime(self.current_dt.year, self.current_dt.month, self.current_dt.day)
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
