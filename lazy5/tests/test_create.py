""" Test creation of HDF5 files """
import os

import pytest

import numpy as np

from lazy5.create import save
from lazy5.utils import FidOrFile


def test_save_no_attrs():
    data = np.random.randn(20,20)
    filename = 'temp_save.h5'
    dset_name = '/Group1/Dset'
    save(filename, dset_name, data, mode='w')

    fof = FidOrFile(filename)
    fid = fof.fid
    assert np.allclose(fid[dset_name], data)
    fof.close_if_file_not_fid()
    
    # Test re-write
    data = np.random.randn(20,20)
    save(filename, dset_name, data, mode='w')
    fof = FidOrFile(filename)
    fid = fof.fid
    assert np.allclose(fid[dset_name], data)
    fof.close_if_file_not_fid()
    
    # Test re-write when overwrite of dset set to False
    data = np.random.randn(20,20)
    with pytest.raises(IOError):
        save(filename, dset_name, data, dset_overwrite=False)
        
    # Test re-write with attributes
    data = np.random.randn(20,20)
    attr_dict = {'AT1':1, 'AT2':2}
    save(filename, dset_name, data, attr_dict=attr_dict, mode='w')

    fof = FidOrFile(filename)
    fid = fof.fid
    assert fid[dset_name].attrs['AT1'] == 1
    assert fid[dset_name].attrs['AT2'] == 2
    with pytest.raises(KeyError):
        fid[dset_name].attrs['DOESNOTEXIST'] == 2
        
    fof.close_if_file_not_fid()

    os.remove(filename)




    # fid['base'].attrs['Attribute_str'] = 'Test'
    # fid['base'].attrs['Attribute_bytes'] = b'Test'
    # fid['base'].attrs['Attribute_np_bytes'] = np.bytes_('Test') # pylint: disable=no-member
    # fid['base'].attrs.create('Attribute_int', 1)
    # fid['base'].attrs.create('Attribute_float', 1.1)
    # fid['base'].attrs.create('Attribute_np_1d', np.array([1, 2, 3]))
    # fid['base'].attrs.create('Attribute_np_2d', np.array([[1, 2, 3], [4, 5, 6]]))