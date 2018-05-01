""" Non-HDF5 utility functions """
import copy as _copy
from collections import OrderedDict as _OrderedDict

def filterlist(in_list, filters, keep_filtered_items=True, exclusive=True):
    """
    Parameters
    ----------
    in_list : list
        List of strings to filter

    filters : str, list, tuple
        Find filters (or entries of filters) in in_list

    keep_filtered_items : bool
        Returns entries from in_list that DO have filters (INCLUDE filter).
        If False, EXCLUDE filter

    exclusive : bool
        Filter is exclusive, i.e. includes/excludes in_list entries that
        have ALL filters. Otherwise, non-exclusive and any entry with A
        filter are excluded/included.

    Returns
    -------
        list : filtered list

    """
    if isinstance(filters, (tuple, list)):
        filter_list = filters
    elif isinstance(filters, str):
        filter_list = [filters]
    else:
        raise TypeError('filters must be of type str, tuple, or list')

    def condition(keep_it, item):
        """ Keep or don't keep item depending on keep_it bool """
        if keep_it:
            return item
        else:
            return not item

    if exclusive:
        out_list = _copy.deepcopy(in_list)
        for current_filt in filter_list:
            out_list = [entry for entry in out_list if condition(keep_filtered_items,
                                                                 entry.count(current_filt))]
    else:
        out_list = []
        for current_filt in filter_list:
            out_list.extend([entry for entry in in_list if condition(keep_filtered_items,
                                                                     entry.count(current_filt))])
            # Removes duplicates
            out_list = list(_OrderedDict.fromkeys(out_list))
    
    return out_list

