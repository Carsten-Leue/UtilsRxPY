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
"""Load the content of file"""
from json import load
from os.path import dirname, join
from typing import Any, Iterable

from pytest import mark
from rx_utils import from_iterable_factory

_ROOT = dirname(__file__)


def _load_file(name: str) -> Iterable[Any]:
    with open(name, 'r', encoding='utf-8') as file_pointer:
        yield load(file_pointer)


@mark.asyncio
async def test_async_files():
    file_ = from_iterable_factory(lambda: _load_file(join(_ROOT, 'data', 'generated.json')))

    result = await file_
    assert result
