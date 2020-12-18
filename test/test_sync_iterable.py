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
from asyncio import AbstractEventLoop
from functools import partial
from glob import iglob
from logging import getLogger
from os.path import dirname, join
from typing import Iterator

from pytest import mark
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
