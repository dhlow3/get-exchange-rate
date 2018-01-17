# -*- coding: utf-8 -*-
"""Test the get_exchange_rate.py module."""
import unittest

from get_exchange_rates import get_google_rate, get_fixer_rate


class ExchangeRateTestCase(unittest.TestCase):
    """Tests for get_exchange_rate.py."""

    def test_google_rate_is_float(self):
        """Is the returned rate a float?"""
        self.assertIsInstance(get_google_rate(['CAD', 'USD']), float)

    def test_fixer_rate_is_float(self):
            """Is the returned rate a float?"""
            self.assertIsInstance(get_fixer_rate(['CAD', 'USD']), float)

if __name__ == '__main__':
    unittest.main()
