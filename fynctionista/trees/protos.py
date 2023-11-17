from typing import Protocol, TypeVar, Callable, Any


T = TypeVar('T')
U = TypeVar('U')


class LinkedList(Protocol[T]):
    def head(self) -> T:
        ...

    def tail(self) -> 'LinkedList':
        ...

    def add(self, item: T) -> 'LinkedList':
        ...

    def pop(self, idx: int = -1) -> tuple[T, 'LinkedList']:
        ...

    def map(self, mapper: Callable[[T], Any]) -> 'LinkedList':
        ...

    def filter(self, filterer: Callable[[T], bool]) -> 'LinkedList':
        ...

    def reduce(self, reducer: Callable[[U, T], U]) -> U:
        ...

    def is_empty(self) -> bool:
        ...

    def __getitem__(self, index: int) -> T:
        ...

    def __len__(self) -> int:
        ...

    def __contains__(self, item: T) -> bool:
        ...

    def __repr__(self) -> str:
        ...
