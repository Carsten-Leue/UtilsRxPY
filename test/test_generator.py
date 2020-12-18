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
from typing import Iterator
from contextlib import contextmanager
from rx_utils import from_iterable_factory
from rx.operators import take


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

    obs = from_iterable_factory(my_generator).pipe(take(2))

    obs.subscribe()

    assert entered
    assert released
