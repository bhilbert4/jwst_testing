"""
This module contains the validation testing for the JWST Calibration
Pipeline.
"""

__docformat__ = 'reStructuredText'

from astropy.io import fits
import numpy as np
import unittest
import pytest

dq_init = pytest.mark.dq_init

@dq_init
class TestDQInitStep:
    """
    The base class for testing the DQInitStep.
    """

    @pytest.fixture
    def hdulist(self, fname):
        """
        Takes the --fname cmd line arg and opens the fits file
        this allows hdulist to be accessible by all test in the class.
        """

        return fits.open(fname)

    def test_groupdq_exists(self, hdulist):
        """
        Checks that the groupdq has been set.
        """
        # if using object from pipeline
        # assert(hasattr(self.dq_init., 'groupdq'))

        # if using fits file generated by strun
        assert("GROUPDQ" in hdulist)

    def test_groupdq_vals(self, hdulist):
        """
        Checks that the groupdq extension 
        values are all zero after dq_init.
        """
        # if using object from pipeline
        # assert(np.all(self.dq_init.groupdq == 0))

        # if using fits file generated by strun
        assert(np.all(hdulist["GROUPDQ"].data == 0))


    def test_err_exists(self, hdulist):
        """
        Check that all err extension values are all zero.
        """

        # if using object from pipeline
        # assert(hasattr(self.dq_init, 'err'))
        # if using fits file generated by strun
        assert("ERR" in hdulist)

    def test_err_vals(self, hdulist):
        """
        Check that all err extension values are all zero.
        """

        # if using object from pipeline
        # assert(np.all(self.dq_init.pixeldq == 0))

        # if using fits file generated by strun
        assert(np.all(hdulist["ERR"].data == 0))
