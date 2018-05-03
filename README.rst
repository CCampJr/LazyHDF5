.. -*- mode: rst -*-

.. image:: https://img.shields.io/travis/CCampJr/LazyHDF5/dev.svg
    :alt: Travis branch
    :target: https://travis-ci.org/CCampJr/LazyHDF5

.. image:: https://img.shields.io/appveyor/ci/CCampJr/LazyHDF5/dev.svg
    :alt: AppVeyor branch
    :target: https://ci.appveyor.com/project/CCampJr/LazyHDF5

.. image:: https://img.shields.io/codecov/c/github/CCampJr/LazyHDF5/dev.svg
    :alt: Codecov branch
    :target: https://codecov.io/gh/CCampJr/LazyHDF5

.. image:: https://img.shields.io/pypi/pyversions/LazyHDF5.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/LazyHDF5/

.. image:: https://img.shields.io/pypi/v/LazyHDF5.svg
    :alt: PyPI
    :target: https://pypi.org/project/LazyHDF5/

.. image:: https://img.shields.io/badge/License-NIST%20Public%20Domain-green.svg
    :alt: NIST Public Domain
    :target: https://github.com/CCampJr/LazyHDF5/blob/dev/LICENSE.md

LazyHDF5: Python Macros for h5py... because I'm lazy
===============================================================

LazyHDF5 is a small package for interacting with HDF5 files. The h5py
library can do-it-all, but it's not necessarily easy to use and
often requires many lines of code to do routine tasks. This package
facilitates easier use.

Also, an HDF5 file viewer written in PyQt5 (optional, not required
for installation) that displaces groups, datasets, and attributes.

- Inspection

    - Get groups, datasets, file hierarchy, dataset attributes

- Editing

    - Write/alter/re-write attributes (coming soon)
    - Repack datasets (coming soon)
    - Copy datasets and files

- Basic file viewer

Dependencies
------------

**Note**: These are the developmental system specs. Older versions of certain
packages may work.

-   python >= 3.4
    
    - Tested with 3.4.6, 3.5.4, 3.6.3

-   numpy (1.9.3)
    
    - Tested with 1.12.1, 1.13.1, 1.13.3

-   h5py (2.7.0)

Optional Dependencies
---------------------

The HDF file view is written in PyQt5; thus, it's necessary **if** you want to
that functionality. All of the other tools in this library are command-line.

-   PyQt5 (5.8)
    
**Note**: PyQt5 only tested on Windows (via AppVeyor)

Known Issues
------------


Installation
------------

Using pip (hard install)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # Only Python 3.* installed
    pip install LazyHDF5

    # If you have both Python 2.* and 3.* you may need
    pip3 install LazyHDF5

Using pip (soft install [can update with git])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::
    
    # Make new directory for LazyHDF5 and enter it
    # Clone from github
    git clone https://github.com/CCampJr/LazyHDF5

    # Only Python 3.* installed
    pip install -e .

    # If you have both Python 2.* and 3.* you may need instead
    pip3 install -e .

    # To update in the future
    git pull

Using setuptools
~~~~~~~~~~~~~~~~

You will need to `download the repository <https://github.com/CCampJr/LazyHDF5>`_
or clone the repository with git:

.. code::
    
    # Make new directory for LazyHDF5 and enter it
    # Clone from github
    git clone https://github.com/CCampJr/LazyHDF5

Perform the install:

.. code::

    python setup.py install

Usage Examples
---------------

1. Getting a list of groups from an un-opened HDF5 file

**Note**: when a filename is provided, the file is opened, queried, and
then closed.

.. code:: python

    from lazy5.inspect import get_groups

    filename = 'SomeFile.h5'
    grp_list = get_groups(filename)

    print('Groups:')
    for grp in grp_list: 
        print(grp)

2. Getting list of datasets from an open HDF5 file

**Note**: when a file-id is provided, the file is queried and
then left open.

.. code:: python

    import h5py
    from lazy5.inspect import get_datasets

    filename = 'SomeFile.h5'
    fid = h5py.File(filename, 'r')

    dset_list = get_datasets(fid)

    print('Datasets:')
    for dset in dset_list: 
        print(dset)

    fid.close()

3. Getting the file hierarchy

.. code:: python

    from lazy5.inspect import get_hierarchy

    filename = 'SomeFile.h5'

    hierarchy = get_hierarchy(filename)

    print('Hierarchy:')
    for k in hierarchy:
        print('{} : {}'.format(k, hierarchy[k]))
    

NONLICENSE
----------
This software was developed by employees of the National Institute of Standards 
and Technology (NIST), an agency of the Federal Government. Pursuant to 
`title 17 United States Code Section 105 <http://www.copyright.gov/title17/92chap1.html#105>`_, 
works of NIST employees are not subject to copyright protection in the United States and are 
considered to be in the public domain. Permission to freely use, copy, modify, 
and distribute this software and its documentation without fee is hereby granted, 
provided that this notice and disclaimer of warranty appears in all copies.

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER 
EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY 
THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM INFRINGEMENT, 
AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE SOFTWARE, OR ANY 
WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT SHALL NIST BE LIABLE 
FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR 
CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY CONNECTED 
WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR 
OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY OR 
OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT OF THE 
RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.

Contact
-------
Charles H Camp Jr: `charles.camp@nist.gov <mailto:charles.camp@nist.gov>`_

Contributors
-------------
Charles H Camp Jr
