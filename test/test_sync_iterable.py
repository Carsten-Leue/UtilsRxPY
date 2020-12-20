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
from threading import current_thread
from time import sleep
from asyncio import AbstractEventLoop
from functools import partial
from glob import iglob
from logging import getLogger
from os.path import dirname, join
from typing import Iterator

from pytest import mark
import pytest
import rx.operators as op
from rx_utils import from_iterable_factory

logger = getLogger(__name__)

_ROOT = dirname(__file__)


def _list_files() -> Iterator[str]:
    return iglob(join(_ROOT, '**', '*.*'), recursive=True)


@mark.asyncio
async def test_sync_iterable():
    obs_ = from_iterable_factory(_list_files).pipe(
        op.take(3),
        op.do_action(print)
    )

    await obs_

def _slow_list_files() -> Iterator[str]:

    def _map_wait(data: str) -> str:
        sleep(0.5)
        return data

    return map(_map_wait, iglob(join(_ROOT, '**', '*.*'), recursive=True))

@mark.asyncio
async def test_slow_sync_iterable():
    obs_ = from_iterable_factory(_slow_list_files).pipe(
        op.take(3),
        op.do_action(print)
    )

    await obs_

def _list_with_exception() -> Iterator[str]:

    def _throw_value_error(data: str) -> str:
        if data == 'c':
            raise ValueError(data)
        return data

    return map(_throw_value_error, iter(('a', 'b', 'c', 'd')))

@mark.asyncio
async def test_sync_exception():
  
    obs_ = from_iterable_factory(_list_with_exception).pipe(
        op.do_action(print)
    )

    with pytest.raises(ValueError):
        await obs_
