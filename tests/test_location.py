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
import math
import unittest

import rubin_sim.utils as simsUtils
from lsst.ts.dateloc import ObservatoryLocation


class ObservatoryLocationTest(unittest.TestCase):
    def setUp(self):
        # Gemini North
        self.latitude_truth = 19.82396
        self.longitude_truth = -155.46984
        self.height_truth = 4213.0
        self.latitude_rad_truth = math.radians(self.latitude_truth)
        self.longitude_rad_truth = math.radians(self.longitude_truth)

    def test_information_after_standard_creation(self):
        location = ObservatoryLocation(
            self.latitude_rad_truth, self.longitude_rad_truth, self.height_truth
        )
        self.assertEqual(location.latitude, self.latitude_truth)
        self.assertEqual(location.longitude, self.longitude_truth)
        self.assertEqual(location.height, self.height_truth)

    def test_information_after_lsst_configuration(self):
        location = ObservatoryLocation()
        location.for_lsst()
        lsst = simsUtils.Site(name="LSST")
        self.assertAlmostEqual(location.latitude, lsst.latitude, places=4)
        self.assertEqual(location.longitude, lsst.longitude)
        self.assertEqual(location.height, lsst.height)

    def test_information_after_config_dictionary_configuration(self):
        condfdict = {
            "obs_site": {
                "latitude": self.latitude_truth,
                "longitude": self.longitude_truth,
                "height": self.height_truth,
            }
        }
        location = ObservatoryLocation()
        location.configure(condfdict)
        self.assertEqual(location.latitude_rad, self.latitude_rad_truth)
        self.assertEqual(location.longitude_rad, self.longitude_rad_truth)
        self.assertEqual(location.height, self.height_truth)

    def test_information_after_reconfiguration(self):
        location = ObservatoryLocation()
        location.reconfigure(
            self.latitude_rad_truth, self.longitude_rad_truth, self.height_truth
        )
        self.assertEqual(location.latitude_rad, self.latitude_rad_truth)
        self.assertEqual(location.longitude_rad, self.longitude_rad_truth)
        self.assertEqual(location.height, self.height_truth)

    def test_get_configure_dict(self):
        cd = ObservatoryLocation.get_configure_dict()
        self.assertEqual(len(cd), 1)
        self.assertEqual(len(cd["obs_site"]), 3)


if __name__ == "__main__":
    unittest.main()
