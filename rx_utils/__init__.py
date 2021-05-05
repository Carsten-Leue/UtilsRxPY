"""UtilsRxPY"""
from typing import Tuple

# version information
__version__ = '0.0.8'

from ._internal.from_iterable_factory import from_iterable_factory

# Some python nonsense
__all__: Tuple[str, ...] = (
    'from_iterable_factory',
)
