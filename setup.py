"""

"""

from setuptools import setup, find_packages
import lazy5

with open('README.rst') as f:
    long_description = f.read()

print('Version: {}'.format(lazy5.__version__))

setup(name='LazyHDF5',
      version = lazy5.__version__,
      description = 'Python Macros for h5py... because I\'m lazy',
      long_description = long_description,
      url = 'https://github.com/CCampJr/LazyHDF5',
      author = 'Charles H. Camp Jr.',
      author_email = 'charles.camp@nist.gov',
      license = 'Public Domain',
      packages = find_packages(),
      zip_safe = False,
      include_package_data = True,
      install_requires=['numpy', 'h5py>= 2.6.0'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Database',
                   'Topic :: Software Development :: Libraries :: Python Modules'
                  ])