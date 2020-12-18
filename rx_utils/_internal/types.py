"""Some type infos"""

from typing import AsyncIterable, Awaitable, Callable, Iterable, TypeVar, Union


T = TypeVar('T')    # pylint: disable=invalid-name

IterableFactorySync = Callable[[], Iterable[T]]
IterableFactoryAsync = Callable[[], Awaitable[Iterable[T]]]

AsyncIterableFactorySync = Callable[[], AsyncIterable[T]]
AsyncIterableFactoryAsync = Callable[[], Awaitable[AsyncIterable[T]]]

IterableAsync = Awaitable[Iterable[T]]
AsyncIterableAsync = Awaitable[AsyncIterable[T]]

GeneralIterable = Union[Iterable[T], IterableAsync[T], AsyncIterable[T], AsyncIterableAsync[T]]

IterableFactory = Union[IterableFactorySync[T], IterableFactoryAsync[T], AsyncIterableFactorySync[T], AsyncIterableFactoryAsync[T]]
