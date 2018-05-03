""" Macros for inspection of HDF5 files """
from collections import OrderedDict as _OrderedDict

import h5py as _h5py
import numpy as _np

from lazy5.utils import (FidOrFile as _FidOrFile)

__all__ = ['get_groups', 'get_datasets', 'get_hierarchy',
           'get_attrs_dset']

def get_groups(file):
    """
    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    Notes
    -----
    Gets groups in a hierarchical list starting from the base '/'. Thus if
    Group2 is INSIDE Group1, it will return Group1, Group1/Group2 -- NOT Group2
    inidividually.
    """
    # Get fid for a file (str or open fid)
    fof = _FidOrFile(file)
    fid = fof.fid

    all_items_list = []
    fid.visit(all_items_list.append)

    # list-set-list removes duplicates
    grp_list = list(set([item for item in all_items_list if isinstance(fid[item], _h5py.Group)]))

    grp_list.append('/')  # Add in base level group
    grp_list.sort()

    fof.close_if_file_not_fid()

    return grp_list

def get_datasets(file, fulldsetpath=True):
    """
    Parameters
    ----------

    file : str or _h5py.File
        Filename or File-object for open HDF5 file
    """
    # Get fid for a file (str or open fid)
    fof = _FidOrFile(file)
    fid = fof.fid

    all_items_list = []
    fid.visit(all_items_list.append)
    dset_list = []

    # list-set-list removes duplicates
    dset_list = list(set([item for item in all_items_list if isinstance(fid[item], _h5py.Dataset)]))
    dset_list.sort()

    if not fulldsetpath:
        for num, dset in enumerate(dset_list):
            split_out = dset.rsplit('/', maxsplit=1)
            if len(split_out) == 1:
                pass
            else:
                dset_list[num] = split_out[-1]

    fof.close_if_file_not_fid()

    return dset_list

def get_hierarchy(file, fulldsetpath=False, grp_w_dset=False):
    """
    Return an ordered dictionary, where the keys are groups and the items are
    the datasets

    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    fulldsetpath : bool
        If True, a dataset name will be prepended with the group down to the
        base level, '/'. If False, it will just be the dset name.

    grp_w_dset : bool
        If True, only return groups that contain datasets. If False, include
        empty groups

    Returns
    -------
    OrderedDict : (group, [dataset list])
        Group and dataset names

    """

    # Get fid for a file (str or open fid)
    fof = _FidOrFile(file)
    fid = fof.fid

    grp_list = get_groups(fid)
    dset_list = get_datasets(fid, fulldsetpath=True)

    grp_dict = _OrderedDict([[grp, []] for grp in grp_list])

    for dset in dset_list:
        split_out = dset.rsplit('/', maxsplit=1)
        if len(split_out) == 1:
            grp_dict['/'].append(dset)
        else:
            if fulldsetpath:
                grp_dict[split_out[0]].append(dset)
            else:
                grp_dict[split_out[0]].append(split_out[1])

    # Only keep groups with datasets
    if grp_w_dset:
        to_pop = []
        for k in grp_dict:
            if not grp_dict[k]:  # is empty
                to_pop.append(k)

        for empty_grp in to_pop:
            grp_dict.pop(empty_grp)

    fof.close_if_file_not_fid()

    return grp_dict

def get_attrs_dset(file, dset, convert_to_str=True):
    """
    Get dictionary of attribute values for a given dataset

    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    dset : str
        Full dataset name with preprended group names. E.g., '/Group1/Dataset'

    convert_to_str : bool
        If an attribute is a numpy.bytes_ string-like object, but not a str, try
        to decode into utf-8.

    Returns
    -------
    OrderedDict : (key, value)

    """

    # Get fid for a file (str or open fid)
    fof = _FidOrFile(file)
    fid = fof.fid

    ds_attrs = fid[dset].attrs

    attr_keys_list = list(ds_attrs)
    attr_keys_list.sort()

    attr_list = []
    for k in attr_keys_list:
        try:
            attr_val = ds_attrs[k]
        except (TypeError, ValueError):
            print('Could not get value for attribute: {}. Set to None'.format(k))
            attr_list.append([k, None])
        else:
            if (isinstance(attr_val, _np.bytes_) | isinstance(attr_val, bytes)) & convert_to_str: # pylint: disable=no-member
                attr_list.append([k, attr_val.decode()])
            else:
                attr_list.append([k, attr_val])

    attr_dict = _OrderedDict(attr_list)

    fof.close_if_file_not_fid()

    return attr_dict
