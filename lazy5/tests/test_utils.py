""" Test HDF-related utilities """
import os

import pytest

import h5py
import numpy as np

from lazy5.utils import (FidOrFile, hdf_is_open, check_type_compat,
                         return_family_type)

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
    filename, _ = hdf_dataset

    fof = FidOrFile(filename)
    assert fof.fid.fid.valid == 1
    assert fof.fid is not None
    assert not fof.is_fid

    fof.fid.close()

def test_fid_or_file_fid_provided(hdf_dataset):
    """ Test FidOrFile Class with provided fid """
    _, fid = hdf_dataset

    fof = FidOrFile(fid)
    assert fof.fid.fid.valid == 1
    assert fof.fid is not None
    assert fof.is_fid

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
    _, fid = hdf_dataset

    assert hdf_is_open(fid)
    fid.close()

    assert not hdf_is_open(fid)

def test_return_family_type():
    """ Test return_family_type """
    assert return_family_type(1) is int
    assert return_family_type(1.1) is float
    assert return_family_type(1 + 1j*3) is complex
    assert return_family_type('Test') is str
    assert return_family_type(b'Test') is bytes
    assert return_family_type(True) is bool

    assert return_family_type(np.int32(1)) is int
    assert return_family_type(np.int(1)) is int
    assert return_family_type(np.float32(1.1)) is float
    assert return_family_type(np.float(1.1)) is float
    assert return_family_type(np.complex64(1 + 1j*3)) is complex
    assert return_family_type(np.complex(1 + 1j*3)) is complex
    assert return_family_type(np.str('Test')) is str
    assert return_family_type(np.str_('Test')) is str  # pylint: disable=E1101
    assert return_family_type(np.bytes_('Test')) is bytes  # pylint: disable=E1101
    assert return_family_type(np.bool(True)) is bool
    assert return_family_type(np.bool_(True)) is bool

    with pytest.raises(TypeError):
        return_family_type([1, 2, 3])

    with pytest.raises(TypeError):
        return_family_type((1, 2, 3))

    with pytest.raises(TypeError):
        return_family_type({'a':1})


def test_check_type_compat():
    """ Test check_type_compat[ibility] """

    # Positive tests
    assert check_type_compat(1, 2)
    assert check_type_compat(1.1, 2.1)
    assert check_type_compat(1.1+1j*3, 2.1+1j*8)
    assert check_type_compat('Test', 'Test2')
    assert check_type_compat(b'Test', b'Test2')
    assert check_type_compat(True, False)

    assert check_type_compat(1, np.int32(2))
    assert check_type_compat(1.1, np.float32(2.1))
    assert check_type_compat(1.1+1j*3, np.complex64(2.1+1j*8))
    assert check_type_compat('Test', np.str_('Test2'))  # pylint: disable=E1101
    assert check_type_compat(b'Test', np.bytes_('Test2'))  # pylint: disable=E1101
    assert check_type_compat(True, np.bool_(False))

    # Negative checks
    assert not check_type_compat(1, 2.1)
    assert not check_type_compat(1.1, 2)
    assert not check_type_compat(1.1+1j*3, 2.1)
    assert not check_type_compat('Test', 1)
    assert not check_type_compat('Test', b'Test2')
    assert not check_type_compat(True, 1)

    assert not check_type_compat(1.1, np.int32(2))
    assert not check_type_compat(1, np.float32(2.1))
    assert not check_type_compat(1, np.complex64(2.1+1j*8))
    assert not check_type_compat(1, np.str_('Test2'))  # pylint: disable=E1101
    assert not check_type_compat('Test', np.bytes_('Test2'))  # pylint: disable=E1101
    assert not check_type_compat(1, np.bool_(False))
