# +-------------------------------------------------------------------+
# | Licensed Materials - Property of IBM                              |
# |                                                                   |
# | Hosting Appliance                                                 |
# |                                                                   |
# | Copyright IBM Corp. 2020 All Rights Reserved                      |
# |                                                                   |
# | US Government Users Restricted Rights - Use, duplication or       |
# | disclosure restricted by GSA ADP Schedule Contract with IBM Corp. |
# +-------------------------------------------------------------------+

""" Setup file """

from pathlib import Path
from typing import Sequence
from shutil import copy

from setuptools import setup, find_packages


def copy_inv():
    try:
        root = Path(__file__).parent
        copy(root / 'build' / 'docs' / 'objects.inv', root / 'rx_utils' / 'docs')
    except BaseException:
        pass

def read(fname: str) -> str:
    return open(Path(__file__).parent / fname).read()


def read_requirements(filename: str) -> Sequence[str]:
    return read(filename).splitlines()


settings = dict(
    name='UtilsRxPY',
    packages=find_packages(exclude=["test"]),
    version='0.0.3',
    author='Dr. Carsten Leue',
    author_email='carsten.leue@gmx.net',
    description=('This is an awesome project!'),
    license='MIT',
    keywords='UtilsRxPY',
    url='https://github.com/Carsten-Leue/UtilsRxPY',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',        
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Typing :: Typed'
    ],
    zip_safe=False
)

copy_inv()
setup(**settings)
