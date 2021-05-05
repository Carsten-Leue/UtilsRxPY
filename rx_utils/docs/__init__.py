"""Exposes the inverse object mapping for sphinx"""
from typing import Sequence
from os.path import dirname, join, normpath

# version information
__version__ = '0.0.8'


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
