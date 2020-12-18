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
from asyncio import sleep
from logging import getLogger
from typing import AsyncIterator

from pytest import mark
from rx.operators import map, take
from rx_utils import from_iterable_factory

logger = getLogger(__name__)


async def async_my_generator() -> AsyncIterator[int]:
    await sleep(0.1)
    yield 1
    await sleep(0.1)
    yield 2
    await sleep(0.1)
    yield 3


@mark.asyncio
async def test_async_iterable():
    obs_ = from_iterable_factory(async_my_generator).pipe(
        map(lambda x: x * x)
    )

    last = await obs_
    assert last == 9
