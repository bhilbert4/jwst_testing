"""
This module contains the validation testing for the JWST Calibration
Pipeline.
"""

__docformat__ = 'reStructuredText'

from astropy.io import fits
import numpy as np
import unittest
import pytest

@pytest.mark.dq_init
class TestDQInitStep:
    """
    The base class for testing the DQInitStep.
    """
    @pytest.fixture
    def refhdu(self, dq_init_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+dq_init_hdu[0].header['R_MASK'][7:]
        return fits.open(ref_file)

    def test_pixeldq_ext_exists(self, dq_init_hdu):
        assert("PIXELDQ" in dq_init_hdu)

    def test_good_pixeldq_propagation(self, dq_init_hdu, refhdu):
        """
        make sure that the values in the reference mask are properly
        translated to values in PIXELDQ
        """

        pixeldq = dq_init_hdu['PIXELDQ'].data
        #find good/bad pixels
        # check that all good and pixels are preserved 
        good = np.where(refhdu['DQ'].data == 0)
        assert np.all(pixeldq[good] == 0)

    def test_dead_pixeldq_dead_propagtion(self, dq_init_hdu, refhdu):
        """
        make sure that the values in the reference mask are properly
        translated to values in PIXELDQ
        """

        pixeldq = dq_init_hdu['PIXELDQ'].data

        # check dead pixels
        dead = np.where(refhdu['DQ'].data == 3)
        assert np.all(pixeldq[dead] == 1025)

    def test_hot_pixeldq_propagation(self, dq_init_hdu, refhdu):
        """
        make sure that the values in the reference mask are properly
        translated to values in PIXELDQ
        """

        pixeldq = dq_init_hdu['PIXELDQ'].data

        # #check hot pixels
        hot = np.where(refhdu['DQ'].data == 5)
        assert np.all(pixeldq[hot] == 2049)

    def test_unreliable_slope_pixeldq_propagation(self, dq_init_hdu, refhdu):
        """
        make sure that the values in the reference mask are properly
        translated to values in PIXELDQ
        """

        pixeldq = dq_init_hdu['PIXELDQ'].data

        # #check unreliable slope
        urs = np.where(refhdu['DQ'].data == 9)
        assert np.all(pixeldq[urs] == 16777217)

    def test_rc_pixeldq_propagation(self, dq_init_hdu, refhdu):
        """
        make sure that the values in the reference mask are properly
        translated to values in PIXELDQ
        """

        pixeldq = dq_init_hdu['PIXELDQ'].data

        # #check RC pixels
        rc = np.where(refhdu['DQ'].data == 17)
        assert np.all(pixeldq[rc] == 16385)

    def test_groupdq_ext_exists(self, dq_init_hdu):
        """
        Checks that the groupdq has been set.
        """
        # if using object from pipeline
        # assert(hasattr(self.dq_init., 'groupdq'))

        # if using fits file generated by strun
        assert("GROUPDQ" in dq_init_hdu)

    def test_groupdq_vals_all_zero(self, dq_init_hdu):
        """
        Checks that the groupdq extension 
        values are all zero after dq_init.
        """
        # if using object from pipeline
        # assert(np.all(self.dq_init.groupdq == 0))

        # if using fits file generated by strun
        assert(np.all(dq_init_hdu["GROUPDQ"].data == 0))


    def test_err_ext_exists(self, dq_init_hdu):
        """
        Check that all err extension values are all zero.
        """

        # if using object from pipeline
        # assert(hasattr(self.dq_init, 'err'))
        # if using fits file generated by strun
        assert("ERR" in dq_init_hdu)

    def test_err_vals_all_zero(self, dq_init_hdu):
        """
        Check that all err extension values are all zero.
        """

        # if using object from pipeline
        # assert(np.all(self.dq_init.pixeldq == 0))

        # if using fits file generated by strun
        assert(np.all(dq_init_hdu["ERR"].data == 0))

@pytest.mark.saturation
class TestSaturationStep:
    """
    The base class for testing the SaturationStep.
    """

    @pytest.fixture
    def refhdu(self, sat_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+sat_hdu[0].header['R_SATURA'][7:]
        return fits.open(ref_file)

    def test_groupdq_vals(self, sat_hdu, refhdu):
        """
        Check that saturated pixels are flagged properly
        """
        # TODO
        if 'DQ' in refhdu:
            flag = np.logical_and(sat_hdu['SCI'].data > refhdu['SCI'].data, 
                refhdu['DQ'].data != 2)
        else: 
            flag = sat_hdu['SCI'].data > refhdu['SCI'].data
        expected_groupdq = np.zeros_like(sat_hdu['GROUPDQ'].data)
        expected_groupdq[flag] = 2
        assert np.all(sat_hdu['GROUPDQ'].data == expected_groupdq)

    @pytest.mark.dq_init
    def test_saturation_pixeldq_propagation(self, sat_hdu, refhdu, dq_init_hdu):
        """
        check that proper Data Quality flags are added according to reference
        file.
        """
        no_sat_check = np.where(refhdu['DQ'].data == 2)
        pixeldq_change = np.zeros_like(sat_hdu['PIXELDQ'].data)
        pixeldq_change[no_sat_check] = 2097152
        assert np.all(dq_init_hdu['PIXELDQ'].data + pixeldq_change == sat_hdu['PIXELDQ'].data)

@pytest.mark.ipc
class TestIPCStep:
    """
    The base class for testing the IPCStep.
    """

    @pytest.fixture
    def refhdu(self, ipc_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+sat_hdu[0].header['R_IPC'][7:]
        return fits.open(ref_file)

@pytest.mark.superbias
class TestSuperbiasStep:
    """
    The base class for testing the SuperbiasStep
    """

    @pytest.fixture
    def refhdu(self, superbias_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+superbias_hdu[0].header['R_SUPERB'][7:]
        return fits.open(ref_file)

    @pytest.mark.saturation
    def test_superbias_pixeldq_propagation(self, superbias_hdu, refhdu, sat_hdu):
        """
        check that proper Data Quality flags are added according to reference
        file.
        """
        unrealiable_bias = np.where(refhdu['DQ'].data == 2)
        pixeldq_change = np.zeros_like(superbias_hdu['PIXELDQ'].data)
        pixeldq_change[unrealiable_bias] = 4194304
        assert np.all(sat_hdu['PIXELDQ'].data + pixeldq_change == superbias_hdu['PIXELDQ'].data)

# @pytest.mark.refpix
# class TestRefpixStep:
#     """
#     The base class for testing the RefpixStep
#     """
#     @pytest.fixture
#     def refhdu(self, refpix_hdu):
#         if 'R_REFPIX' in refpix_hdu[0].header:
#             CRDS = '/grp/crds/cache/references/jwst/'
#             ref_file = CRDS+superbias_hdu[0].header['R_SUPERB'][7:]
#             return fits.open(ref_file)

@pytest.mark.linearity
class TestLinearityStep:
    """
    The base class for testing the LinearityStep
    """

    @pytest.fixture
    def refhdu(self, linearity_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+linearity_hdu[0].header['R_LINEAR'][7:]
        return fits.open(ref_file)

    def test_linearity_pixeldq_propagation(self, linearity_hdu, refhdu, lastframe_hdu):
        """
        check that proper Data Quality flags are added according to reference
        file.
        """
        nonlinear = np.where(refhdu['DQ'].data == 2)
        no_lin_corr = np.where(refhdu['DQ'].data == 4)
        pixeldq_change = np.zeros_like(linearity_hdu['PIXELDQ'].data)
        pixeldq_change[nonlinear] = 65536
        pixeldq_change[no_lin_corr] = 1048576
        assert np.all(lastframe_hdu['PIXELDQ'].data + pixeldq_change == linearity_hdu['PIXELDQ'].data)

@pytest.mark.dark_current
class TestDarkCurrentStep:
    """
    The base class for testing the DarkCurrentStep
    """

    @pytest.fixture
    def refhdu(self, dark_current_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+dark_current_hdu[0].header['R_DARK'][7:]
        return fits.open(ref_file)

    def test_dark_current_pixeldq_propagation(self, dark_current_hdu, refhdu, linearity_hdu):
        """
        check that proper Data quality flags are added according to the reference file.
        """

        # warm = np.where(refhdu['DQ'].data == 2)
        # hot = np.where(refhdu['DQ'].data == 4)
        # unreliable_dark = np.where(refhdu['DQ'] == 8)
        # unreliable_slope = np.where

