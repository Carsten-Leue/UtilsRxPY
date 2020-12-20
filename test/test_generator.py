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
"""Test the use of a generator to build an observable"""
from typing import Iterator, List
from contextlib import contextmanager
from rx_utils import from_iterable_factory
import rx.operators as op


def test_iterator():

    data = ('a', 'b', 'c')

    result = list()

    def add_to_list(dst: List[str], item: str) -> List[str]:
        dst.append(item)
        return dst

    obs = from_iterable_factory(lambda: data).pipe(op.take(2), op.reduce(add_to_list, result))
    obs.subscribe()

    assert len(result) == 2
    assert result == ['a', 'b']


def test_generator():

    entered = False
    released = False

    @contextmanager
    def my_context():
        nonlocal entered
        nonlocal released
        entered = True
        try:
            yield
        finally:
            released = True

    def my_generator() -> Iterator[int]:
        with my_context():
            yield 1
            yield 2
            yield 3

    obs = from_iterable_factory(my_generator).pipe(op.take(2))

    obs.subscribe()

    assert entered
    assert released
