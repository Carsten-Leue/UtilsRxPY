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

"""UtilsRxPY"""
from typing import Tuple

# version information
__version__ = '0.0.5'

from ._internal.from_iterable_factory import from_iterable_factory

# Some python nonsense
__all__: Tuple[str, ...] = (
    'from_iterable_factory',
)
