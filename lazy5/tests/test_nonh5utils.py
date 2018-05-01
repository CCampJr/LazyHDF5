""" Test non-HDF-related utilities """
import os

import pytest

import numpy as np

from lazy5.nonh5utils import filterlist

def test_filter_list():
    """ Test filtering of lists """
    list_to_filter = ['Keep1', 'Keep2', 'KeepExclude', 'Exclude1', 'Exclude2']

    # Keep, filter=str, exclusive
    filters = 'Keep'
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True, 
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Exclude, filter=str, exclusive
    filters = 'Exclude'
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False, 
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2']

    # Keep, filter=list, exclusive
    filters = ['Keep']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True, 
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Keep, filter=tuple, exclusive
    filters = ('Keep')
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True, 
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Keep, filter=list, exclusive
    filters = ['Keep','1']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True, 
                          exclusive=True)
    assert out_list == ['Keep1']

    # Keep, filter=list, NOT-exclusive
    filters = ['Keep', '1']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True, 
                          exclusive=False)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude', 'Exclude1']

    # Exclude, filter=list, exclusive
    filters = ['Exclude','2']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False, 
                          exclusive=True)
    assert out_list == ['Keep1']

    # Exclude, filter=list, NON-exclusive
    filters = ['Exclude','2']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False, 
                          exclusive=False)
        
    assert out_list == ['Keep1','Keep2','KeepExclude','Exclude1']

    # Wrong type of filter
    filters = 1
    with pytest.raises(TypeError):
        out_list = filterlist(list_to_filter, filters, keep_filtered_items=False, 
                              exclusive=False)


