""" Test HDF-related utilities """
import os

import pytest

import h5py
import numpy as np

from lazy5.utils import FidOrFile, hdf_is_open

@pytest.fixture(scope="module")
def hdf_dataset():
    """ Setups and tears down a sample HDF5 file """
    filename = 'temp_test_utils.h5'
    fid = h5py.File(filename, 'w')
    data_m, data_n, data_p = [20, 22, 24]
    data = np.random.randn(data_m, data_n, data_p)
    fid.create_dataset('base', data=data)

    yield filename, fid

    # Tear-down
    if hdf_is_open(fid):
        fid.close()
    os.remove(filename)

def test_fid_or_file_filename_provided(hdf_dataset):
    """ Test FidOrFile Class with provided filename """
    filename, fid = hdf_dataset

    fof = FidOrFile(filename)
    assert fof.fid.fid.valid == 1
    assert fof.fid is not None
    assert fof.is_fid == False

    fof.fid.close()

def test_fid_or_file_fid_provided(hdf_dataset):
    """ Test FidOrFile Class with provided fid """
    filename, fid = hdf_dataset

    fof = FidOrFile(fid)
    assert fof.fid.fid.valid == 1
    assert fof.fid is not None
    assert fof.is_fid == True

def test_fid_or_file_close_if_not_fid(hdf_dataset):
    """ Test close if filename was provided """
    filename, fid = hdf_dataset

    fof = FidOrFile(fid)
    fof.close_if_file_not_fid()
    assert fof.fid.fid.valid == 1

    fof = FidOrFile(filename)
    fof.close_if_file_not_fid()
    assert fof.fid.fid.valid == 0

def test_hdf_is_open(hdf_dataset):
    """ Test hdf_is_open function """
    filename, fid = hdf_dataset

    assert hdf_is_open(fid) == True
    fid.close()
    
    assert hdf_is_open(fid) == False
