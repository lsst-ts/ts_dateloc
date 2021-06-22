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
