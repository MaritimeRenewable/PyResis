# -*- coding: utf-8 -*-
import logging
from unittest import TestCase

from PyResis.ship import Ship

LOG = logging.getLogger(__name__)


class Main(TestCase):
    r"""
    test for base functionality
    """

    def test_main(self):
        r"""
        test for general call
        """
        self.assertEqual(0.1611291212508747, Ship(5.72, 0.248, 0.76, 0.2, 6.99, 0.613).propulsion_power())
