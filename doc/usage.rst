=====
Usage
=====

The classes in this module are mainly used to support other packages. However, a brief demonstration of each class will be given. 

ObservatoryLocation
===================

As its name implies, this class is used to store position information for an observatory location. For those wanting to get the LSST location, do the following.

.. code-block:: python

  from lsst.ts.dateloc import ObservatoryLocation
  lsst = ObservatoryLocation()
  lsst.for_lsst()

For other observatories, the information can be passed during instance creation, via a dictionary and a reconfiguration method. The next example will be for Gemini North and show the three variations. 

.. code-block:: python

  import math
  from lsst.ts.dateloc import ObservatoryLocation
  gemini_north = ObservatoryLocation(math.radians(19.82396), math.radians(-155.46984), 4213.0)

.. code-block:: python

  import math
  from lsst.ts.dateloc import ObservatoryLocation
  gemini_north = ObservatoryLocation()
  confdict = {"obs_site": {"latitude": 19.82396, "longitude": -155.46984, "height": 4213.0}}
  gemini_north.configure(confdict)

.. code-block:: python

  import math
  from lsst.ts.dateloc import ObservatoryLocation
  gemini_north = ObservatoryLocation()
  gemini_north.reconfigure(math.radians(19.82396), math.radians(-155.46984), 4213.0)

See the API documentation for :py:class:`.ObservatoryLocation`.

DateProfile
===========

This class handles date manipulation concerning Modified Julian Dates and Local Sidereal Times. It requires an :py:class:`ObservatoryLocation` instance to work. We will use the `lsst` instance from the previous section's example. To create an instance, do the following.

.. code-block:: python

  from lsst.ts.dateloc import DateProfile
  dp = DateProfile(0, lsst)

The first argument is a UTC timestamp, but in this case we used a default value. The timestamp stored can be updated. We will use the timestamp from July 14, 2017 at 02:40 UTC.

.. code-block:: python

  dp.update(1500000000)
  dp.mjd
  57948.11111111111
  dp.lst_rad
  4.562528854015541

See the API documentation for :py:class:`.DateProfile`.
