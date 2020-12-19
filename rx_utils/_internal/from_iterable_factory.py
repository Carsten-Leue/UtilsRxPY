"""Creates an iterator from a factory of iterables"""
from asyncio import AbstractEventLoop, CancelledError
from functools import partial, reduce
from inspect import isawaitable
from itertools import takewhile
from logging import getLogger
from typing import Any, AsyncIterable, Iterable, Optional, Union, cast

import rx.operators as op
from rx import Observable, defer, empty, from_iterable
from rx.core.typing import Action, OnNext, Predicate, Scheduler
from rx.scheduler.eventloop import AsyncIOScheduler

from .async_utils import from_async
from .types import (AsyncIterableAsync, GeneralIterable, IterableAsync,
                    IterableFactory, T)

logger = getLogger(__name__)


def _noop():
    pass


def _is_iterable(obj: Any) -> bool:
    return callable(getattr(obj, '__iter__', None))


def _is_asynciterable(obj: Any) -> bool:
    return callable(getattr(obj, '__aiter__', None))


async def _async_noop():
    pass


async def _from_async_iterable(iterable: AsyncIterable[T], on_next: OnNext, loop: AbstractEventLoop):
    #: sanity check
    assert iterable
    assert callable(on_next)
    assert loop
    #: close callback
    done = getattr(iterable, 'aclose', _async_noop)
    try:
        async for value in iterable:
            loop.call_soon(on_next, value)
    finally:
        #: resource cleanup
        await done()


def _sync_generate(iterable: Iterable[T], on_next: OnNext, is_running: Predicate[T]):
    #: sanity checks
    assert callable(on_next)
    assert callable(is_running)

    done: Action = getattr(iterable, 'close', _noop)

    try:
        reduce(lambda _, item: on_next(item), takewhile(is_running, iter(iterable)), None)
    finally:
        done()


async def _async_generate(iterable: Iterable[T], on_next: OnNext, loop: AbstractEventLoop):
    #: sanity checks
    assert callable(on_next)
    assert loop

    #: cancelation flag
    is_running = True
    try:
        await loop.run_in_executor(None,
                                   _sync_generate,
                                   iterable,
                                   partial(loop.call_soon_threadsafe, on_next),
                                   lambda _: is_running
                                   )
    except CancelledError:
        is_running = False


async def _async_from_async(iterable: Union[AsyncIterable[T], Iterable[T]], on_next: OnNext, loop: AbstractEventLoop):
    #: check for a regular iterable
    if _is_iterable(iterable):
        await _async_generate(cast(Iterable[T], iterable), on_next, loop)
    elif _is_asynciterable(iterable):
        await _from_async_iterable(cast(AsyncIterable[T], iterable), on_next, loop)
    else:
        logger.warning('Object of type [%s] is neither Iterable nor AsyncIterable.', type(iterable))


def _from_async(scheduler: Optional[Scheduler], iterable: Union[AsyncIterableAsync[T], IterableAsync[T]]) -> Observable:
    #: sanity check
    assert isawaitable(iterable)

    async def _dispatch(on_next: OnNext, loop: AbstractEventLoop):
        await _async_from_async(await iterable, on_next, loop)

    return from_async(_dispatch, scheduler)


def _from_sync(scheduler: Optional[Scheduler], iterable: Union[AsyncIterable[T], Iterable[T]]) -> Observable:
    #: sanity check
    assert not isawaitable(iterable)

    #: check for a regular iterable
    if _is_iterable(iterable):
        return from_iterable(cast(Iterable[T], iterable), scheduler)

    async def _dispatch(on_next: OnNext, loop: AbstractEventLoop):
        await _from_async_iterable(cast(AsyncIterable[T], iterable), on_next, loop)

    #: check for an sync iterable
    if _is_asynciterable(iterable):
        return from_async(_dispatch, scheduler)

    logger.warning('Object of type [%s] is neither Iterable nor AsyncIterable.', type(iterable))

    return empty(scheduler)


async def _async_from_iterable_factory_on_async_scheduler(factory: IterableFactory[T], on_next: OnNext, loop: AbstractEventLoop):
    #: construct the resource
    iterable: GeneralIterable[T] = factory()

    if isawaitable(iterable):
        await _async_from_async(await cast(Union[AsyncIterableAsync[T], IterableAsync[T]], iterable), on_next, loop)
    else:
        await _async_from_async(cast(Union[AsyncIterable[T], Iterable[T]], iterable), on_next, loop)


def _from_iterable_factory_on_async_scheduler(factory: IterableFactory[T], scheduler: AsyncIOScheduler) -> Observable:

    async def _dispatch(on_next: OnNext, loop: AbstractEventLoop):
        await _async_from_iterable_factory_on_async_scheduler(factory, on_next, loop)

    return from_async(_dispatch, scheduler)


def _from_iterable_factory_on_scheduler(factory: IterableFactory[T], scheduler: Optional[Scheduler]) -> Observable:
    #: construct the resource
    iterable: GeneralIterable[T] = factory()
    done: Action = getattr(iterable, 'close', _noop)
    #: ensure cleanup
    return (_from_async if isawaitable(iterable) else _from_sync)(scheduler, iterable).pipe(op.finally_action(done))


def _from_iterable_factory(factory: IterableFactory[T], base_scheduler: Optional[Scheduler], scheduler: Optional[Scheduler]) -> Observable:
    #: the scheduler
    scheduler = scheduler or base_scheduler

    if isinstance(scheduler, AsyncIOScheduler):
        return _from_iterable_factory_on_async_scheduler(factory, scheduler)

    return _from_iterable_factory_on_scheduler(factory, scheduler)


def from_iterable_factory(factory: IterableFactory[T], scheduler: Optional[Scheduler] = None) -> Observable:
    """Constructs an observable for an sync or async iterable factory. Each subscription will create
    a new iterable via the factory, this allows e.g. to iterate multiple times over generators. If the object
    returned by the iterable factory is closeable (sync or async) then it will be closed when the
    observable gets unsubscribed. This is e.g. the case for generators.

    Args:
        factory: the iterable factory, may be sync or async
        scheduler: Optionally a scheduler. Defaults to None.

    Returns:
        the observable
    """
    #: quick sanity check
    assert callable(factory)
    #: dispatch
    return defer(partial(_from_iterable_factory, factory, scheduler))
