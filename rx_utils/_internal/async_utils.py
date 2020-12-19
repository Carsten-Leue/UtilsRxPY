"""Some general purpose utilities"""
import asyncio
from asyncio import (AbstractEventLoop, CancelledError, ensure_future,
                     iscoroutinefunction)
from functools import partial
from logging import getLogger
from typing import Any, Awaitable, Callable, Optional, TypeVar

from rx import Observable
from rx import create as rx_create
from rx.core.typing import Action, Observer, OnNext, Scheduler, TState
from rx.disposable import Disposable

T = TypeVar('T', covariant=True)    # pylint: disable=invalid-name

logger = getLogger(__name__)

_get_loop = getattr(asyncio, 'get_running_loop', None) or getattr(asyncio, '_get_running_loop')
assert callable(_get_loop)


async def _async_subscribe(generator: Callable[[OnNext, AbstractEventLoop], Awaitable], observer: Observer[T], event_loop: Optional[AbstractEventLoop]):
    #: sanity check
    assert observer
    #: access the event loop
    loop = event_loop or _get_loop()

    try:
        #: log this
        logger.debug('[%s]: Subscribing...')
        #: produce the value and dispatch
        await generator(observer.on_next, loop)
        loop.call_soon(observer.on_completed)
        #: log this
        logger.debug('[%s]: Completed')
    except CancelledError:
        loop.call_soon(observer.on_completed)
        #: log this
        logger.debug('[%s]: Canceled')
    except Exception as ex:  # pylint: disable=broad-except
        #: log this
        logger.exception('[%s]: Error')
        #: dispatch the error
        loop.call_soon(observer.on_error, ex)


def _create_action(delegate: Callable[[], Any]) -> Action:

    def _dispatch():
        delegate()

    return _dispatch


def _create_disposable(generator: Callable[[OnNext, AbstractEventLoop], Awaitable], observer: Observer[T], loop: Optional[AbstractEventLoop] = None) -> Disposable:
    return Disposable(_create_action(ensure_future(_async_subscribe(generator, observer, loop), loop=loop).cancel))


def _scheduled_action(generator: Callable[[OnNext, AbstractEventLoop], Awaitable], observer: Observer[T], loop: AbstractEventLoop, _scheduler: Scheduler, _state: Optional[TState]) -> Disposable:
    return _create_disposable(generator, observer, loop)


def _on_subscribe(generator: Callable[[OnNext, AbstractEventLoop], Awaitable], base_scheduler: Optional[Scheduler], observer: Observer[T], scheduler: Optional[Scheduler]):
    #: sanity check
    assert observer
    #: make sure to access the default scheduler
    sched: Optional[Scheduler] = base_scheduler or scheduler

    if sched is not None:
        return sched.schedule(partial(_scheduled_action, generator, observer, getattr(sched, '_loop', None)))

    logger.warning('No scheduler available')
    return _create_disposable(generator, observer)


def from_async(generator: Callable[[OnNext, AbstractEventLoop], Awaitable], scheduler: Optional[Scheduler] = None) -> Observable:
    """Creates an observable from a generic generator

    Args:
        generator: the async generator that produces the result
        scheduler: optionally the scheduler to run on

    Returns:
        observable that represents this operation
    """
    assert iscoroutinefunction(generator)

    return rx_create(partial(_on_subscribe, generator, scheduler))
