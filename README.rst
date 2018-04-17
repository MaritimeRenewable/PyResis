PyResis
=======
A Python package for ship Resistance estimation
[![DOI](https://zenodo.org/badge/103379381.svg)](https://zenodo.org/badge/latestdoi/103379381)

============
Requirement: ``Python >= 3`` and ``numpy, scipy``.

Installation: ``pip install PyResis``.


Usage
=====

To estimate propulsion resistance of a ship with following dimensions at 2 m/s:

..  table::
======================= ====== =======
Dimensions               Value   Unit
======================= ====== =======
Length                  5.72   metres
Draught                 0.248  metres
Beam                    0.76   metres
Slenderness coefficient 6.99
Prismatic coefficient   0.613
======================= ====== =======

With PyResis it is easy to get an resistance estimation by:

.. code-block:: python

   from PyResis import propulsion_power
   ship = propulsion_power.Ship()
   ship.dimension(5.72, 0.248, 0.76, 2, 6.99, 0.613)
   ship.resistance()

Propulsion power estimation:

.. code-block:: python

    ship.prop_power()

