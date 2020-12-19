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

"""Exposes the inverse object mapping for sphinx"""
from typing import Sequence
from os.path import dirname, join, normpath

# version information
__version__ = '0.0.3'


def get_objects_inv_path() -> str:
    """Returns the pathname of the object.inv file

    Returns:
        the pathname
    """
    return normpath(join(dirname(__file__), 'objects.inv'))


# Some python nonsense
__all__: Sequence[str] = (
    'get_objects_inv_path',
)
