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

from __future__ import division

import unittest

from lsst.ts.dateloc import DateProfile, ObservatoryLocation

"""Set timestamp as 2022-01-01 0h UTC"""
LSST_START_TIMESTAMP = 1640995200.0
"""Set MJD for 2022-01-01 0h UTC"""
LSST_START_MJD = 59580.0


class DateProfileTest(unittest.TestCase):
    def setUp(self):
        self.lsst_site = ObservatoryLocation()
        self.lsst_site.for_lsst()
        self.dp = DateProfile(LSST_START_TIMESTAMP, self.lsst_site)

    def test_basic_information_after_creation(self):
        self.assertEqual(self.dp.timestamp, LSST_START_TIMESTAMP)
        self.assertIsNotNone(self.dp.location)
        self.assertIsNotNone(self.dp.current_dt)
        self.assertEqual(self.dp.mjd, LSST_START_MJD)
        self.assertAlmostEqual(self.dp.lst_rad, 0.5215154816963141)

    def test_update_mechanism(self):
        new_timestamp = LSST_START_TIMESTAMP + 3600.0
        self.dp.update(new_timestamp)
        self.assertEqual(self.dp.timestamp, new_timestamp)
        self.assertEqual(self.dp.mjd, LSST_START_MJD + (1.0 / 24.0))
        self.assertEqual(self.dp.lst_rad, 0.7840316524739084)

    def test_call_mechanism(self):
        new_timestamp = LSST_START_TIMESTAMP + (2.0 * 3600.0)
        (mjd, lst_rad) = self.dp(new_timestamp)
        self.assertEqual(mjd, LSST_START_MJD + (2.0 / 24.0))
        self.assertAlmostEqual(lst_rad, 1.0465478232515026, delta=1e-7)

    def test_negative_lst(self):
        new_timestamp = LSST_START_TIMESTAMP + (18.0 * 3600.0)
        (mjd, lst_rad) = self.dp(new_timestamp)
        self.assertEqual(mjd, LSST_START_MJD + (18.0 / 24.0))
        self.assertAlmostEqual(lst_rad, 5.246806555968448, delta=1e-7)

    def test_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(self.dp.midnight_timestamp(), LSST_START_TIMESTAMP)

    def test_next_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(
            self.dp.next_midnight_timestamp(),
            LSST_START_TIMESTAMP + (24.0 * 60.0 * 60.0),
        )

    def test_previous_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(
            self.dp.previous_midnight_timestamp(),
            LSST_START_TIMESTAMP - (24.0 * 60.0 * 60.0),
        )


if __name__ == "__main__":
    unittest.main()
