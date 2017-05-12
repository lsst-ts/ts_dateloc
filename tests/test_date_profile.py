from __future__ import division
import unittest

from lsst.ts.dateloc import DateProfile, ObservatoryLocation
import lsst.utils.tests

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
        self.assertEqual(self.dp.lst_rad, 0.5215154816963141)

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
        self.assertAlmostEqual(lst_rad, 1.0465478232515026, delta=1E-7)

    def test_negative_lst(self):
        new_timestamp = LSST_START_TIMESTAMP + (18.0 * 3600.0)
        (mjd, lst_rad) = self.dp(new_timestamp)
        self.assertEqual(mjd, LSST_START_MJD + (18.0 / 24.0))
        self.assertAlmostEqual(lst_rad, 5.246806555968448, delta=1E-7)

    def test_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(self.dp.midnight_timestamp(), LSST_START_TIMESTAMP)

    def test_next_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(self.dp.next_midnight_timestamp(), LSST_START_TIMESTAMP + (24.0 * 60.0 * 60.0))

    def test_previous_midnight_timestamp(self):
        new_timestamp = LSST_START_TIMESTAMP + (4.0 * 3600.0)
        self.dp.update(new_timestamp)
        self.assertEqual(self.dp.previous_midnight_timestamp(), LSST_START_TIMESTAMP - (24.0 * 60.0 * 60.0))

class MemoryTestClass(lsst.utils.tests.MemoryTestCase):
    pass

def setup_module(module):
    lsst.utils.tests.init()

if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
